# Copyright (c) 2025 Mage Data. All Rights Reserved.
# This file is part of Mage Data SDK, which is licensed under a proprietary license.
# See the LICENSE file in the package root for license terms.

import requests
import logging
import json
import time
from typing import List, Dict, Any, Optional, Union
from jsonpath_ng import parse as parse_jsonpath
from jsonpath_ng.exceptions import JsonPathParserError
from .models import JSONFieldMapping, MappingType, DCType
from .exceptions import (
    AnonymizationError,
    APIError,
    ConfigurationError,
    ValidationError
)

logger = logging.getLogger(__name__)

class AnonymizationClient:
    """Client for interacting with the Mage Data REST APIs"""

    def __init__(
            self,
            base_url: str,
            anon_api_port: int,
            analyze_api_port: int,
            anonymize_api_port: int,
            api_key: str,
            timeout: int = 30,
            retries: int = 3,
            retry_delay: int = 1
    ):
        """
        Initialize the client

        Args:
          base_url: Base URL for the API (optional, provide below 2 urls if base url is not available)
          anon_api_url: URL for the anonymization API
          isecure_api_url: URL for the iSecure API
          timeout: Request timeout in seconds
          retries: Number of retries in case of failure
          retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url
        self.anon_api_port = anon_api_port
        self.analyze_api_port = analyze_api_port
        self.anonymize_api_port = anonymize_api_port
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay

        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        })
        self.port_mapping = {
            "api/anon/data": self.anon_api_port,
            "analyze": self.analyze_api_port,
            "anonymize": self.anonymize_api_port
        }

        self._json_path_cache = {}


    def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict] = None
    ) -> Dict:
        """Make HTTP call with retry logic"""
        
        port = self.port_mapping.get(endpoint)
        url = f"{self.base_url}:{port}/{endpoint}"
        #print(f"url: {url}")
        #print(f"data: {data}")

        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method,
                    url,
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retries}): {e}")
                if attempt == self.retries - 1:
                    raise APIError(f"API request failed after {self.retries} attempts: {str(e)}")
                time.sleep(self.retry_delay * (attempt + 1))
    

    def anonymize_values(
            self,
            dc_name: str,
            values: List[str],
            parameters: Optional[Dict[str, Any]] = None # For future use
    ) -> List[str]:
        """Anonymize a list of values using anonymization api"""

        try:
            response = self._make_request(
                method="POST",
                endpoint="api/anon/data",
                data={
                    "dc_name": dc_name,
                    "values": values
                }
            )
            return list(response.values())
        except Exception as e:
            raise AnonymizationError(f"Anonymization failed: {str(e)}")
        
    def anonymize_text(
            self,
            text: str,
            dc_names: List[str],
            language: str = "en",
            parameters: Optional[Dict[str, Any]] = None # For future use
    ) -> str:
        """Anonymize text using iSecure api"""
        """ 
        Two calls to be made here, one for analyze with the list of DCs to detect.
        And another call to anonymize with the analyzer results
        """
        try:
            #print(f"text: {text}")
            #print(f"dc_names: {dc_names}")

            analyzer_response = self._make_request(
                method="POST",
                endpoint="analyze",
                data={
                    "text": text,
                    "dc_names": dc_names,
                    "language": language or "en"
                }
            )

            #print(f"Analyzer Response: {analyzer_response}")
        
            response = self._make_request(
                method="POST",
                endpoint="anonymize",
                data={
                    "text": text,
                    "analyzer_results": analyzer_response
                }
            )
            #print(f"response: {response["text"]}")
            return [response["text"]]
        
        except Exception as e:
            raise AnonymizationError(f"Anonymization failed: {str(e)}")
        
        
    def _get_compiled_path(self, json_path: str):
        """ Get or compile a JSONPath expression """
        if json_path not in self._json_path_cache:
            try:
                self._json_path_cache[json_path] = parse_jsonpath(json_path)
            except JsonPathParserError as e:
                raise ValidationError(f"Invalid JSONPath '{json_path}': {str(e)}")
            except Exception as e:
                raise ValidationError(f"Error compiling JSONPath '{json_path}': {str(e)}")
        return self._json_path_cache[json_path]
            
    def anonymize_json(
            self,
            json_doc: Dict,
            field_mappings: List[JSONFieldMapping]
    ) -> Dict:
        """
        Anonymize a JSON document based on field mappings

        Args:
        json_doc: JSON document to anonymize
        field_mappings: List of field mapping configurations

        Returns:
        Anonymized JSON document
        """
        if json_doc is None:
            return None
        
        doc_copy = json.loads(json.dumps(json_doc))
        #print(f"field_mappings: {field_mappings}")
        
        for mapping in field_mappings:
            try:
                #print(f"mapping.json_path: {mapping.json_path}")
                #print(f"doc_copy: {doc_copy}")
                #print(f"{parse_jsonpath(mapping.json_path)}")
                #print(f"{parse_jsonpath(mapping.json_path).find(doc_copy)}")
                jsonpath_expr = self._get_compiled_path(mapping.json_path)

                #print(f"jsonpath_expr: {jsonpath_expr}")

                matches = jsonpath_expr.find(doc_copy)
                if not matches:
                    logger.debug(f"No matches found for JSONPath '{mapping.json_path}'")
                    continue
                self._process_json_matches(matches, mapping, doc_copy)
            except AnonymizationError:
                raise
            except Exception as e:
                logger.error(f"Error processing JSONPath {mapping.json_path} : {str(e)}")
                raise AnonymizationError(f"JSON anonymization failed: {str(e)}")
        
        return doc_copy
    
    def _process_json_matches(
            self,
            matches: List,
            mapping: JSONFieldMapping,
            doc: Dict
    ) -> None:
        """Process matches based on mapping type"""

        values = [match.value for match in matches]

        if all(value is None for value in values):
            return
        
        values_for_api=[]
        for value in values:
            if value is None:
                values_for_api.append(None)
            elif not isinstance(value, str):
                values_for_api.append(str(value))
            else:
                values_for_api.append(value)
        
        anonymized_values = self._anonymize_json_values(values_for_api, mapping)

        for match, anonymized_value in zip(matches, anonymized_values):
            if anonymized_value is not None:
                try:
                    match.full_path.update(doc, anonymized_value)
                except Exception as e:
                    logger.error(f"Error updating JSON: {str(e)}")
                    raise AnonymizationError(f"Failed to update JSON: {str(e)}")
                
    def _anonymize_json_values(
            self,
            values: List[str],
            mapping: JSONFieldMapping
    ) -> List[str]:
        """ Anonymize values based on mapping type """
        none_indices = [i for i, v in enumerate(values) if v is None]
        non_none_values = [v for v in values if v is not None]

        if not non_none_values:
            return values
        
        try:
            if mapping.mapping_type == MappingType.SIMPLE:
                if not mapping.dc_types:
                    raise ValidationError(f"Missing DC Type for json path : {mapping.json_path}")
                
                anonymized_values = self.anonymize_values(
                    dc_name=mapping.dc_types[0].value,
                    values=non_none_values,
                    parameters=mapping.parameters
                )
            
            elif mapping.mapping_type == MappingType.DESCRIPTIVE:
                if not mapping.dc_types:
                    raise ValidationError(f"Missing Detect Categories for json path : {mapping.json_path}")

                anonymized_values = []
                for text in non_none_values:
                    if not text.strip():
                        anonymized_values.append(text)
                        continue
                    dc_names = [cat.value for cat in mapping.dc_types]
                    anonymized_text = self.anonymize_text(
                        text=text,
                        dc_names=dc_names,
                        language="en",
                        parameters=mapping.parameters
                    )
                    anonymized_values.append(anonymized_text)
            
            else:
                raise ValidationError(f"Unsupported mapping type: {mapping.mapping_type}")
            
            result = []
            non_none_idx = 0

            for i in range(len(values)):
                if i in none_indices:
                    result.append(None)
                else:
                    result.append(anonymized_values[non_none_idx])
                    non_none_idx += 1
            
            return result
        
        except AnonymizationError:
            raise
        except Exception as e:
            logger.error(f"Error anonymizing values: {str(e)}")
            raise AnonymizationError(f"Failed to anonymize values: {str(e)}")
        
    
    def batch_anonymize_json(
            self,
            json_docs: List[Dict],
            field_mappings: List[JSONFieldMapping]
    ) -> List[Dict]:
        """ Anonymize multiple JSON documents """
        return [self.anonymize_json(doc, field_mappings) for doc in json_docs]
            
    