# Copyright (c) 2025 Mage Data. All Rights Reserved.
# This file is part of Mage Data SDK, which is licensed under a proprietary license.
# See the LICENSE file in the package root for license terms.

from typing import Any, Dict, List, Tuple
from .models import *
from .client import AnonymizationClient

class DataProcessor:
    """Base class for data processing"""
    def __init__(self, client: AnonymizationClient):
        self.client = client

    def process_value(self, value: Any, mapping: ColumnMapping) -> Any:
        """Base class for processing values"""
        raise NotImplementedError
    
class ColumnProcessor(DataProcessor):
    """Processor for simple column values"""
    def process_value(self, value: Any, mapping: ColumnMapping) -> Any:
        if value is None:
            return None
        
        #print(f"Mapping type: {mapping.mapping_type.value}")
        #print(f"DC types: {mapping.dc_types[0].value}")
        #print(f"Value: {value}")
    
        if mapping.mapping_type.value == MappingType.DESCRIPTIVE.value:
            #print("Calling anonymize text...")
            result = self.client.anonymize_text(
                text=str(value),
                dc_names=[dc_type.value for dc_type in mapping.dc_types],
                language="en",
            )
        else:
            #print("Calling anonymize values...")
            result = self.client.anonymize_values(
                dc_name=mapping.dc_types[0].value,     #send only first value since api can only take one
                values=[str(value)],
            )

        #print(f"Result: {result}")
        
        return result[0]
    
class JSONProcessor(DataProcessor):
    """Processor for JSON column values"""
    def process_value(self, value: Dict, mapping: JSONColumnMapping) -> Dict:
        if value is None:
            return None
        result = self.client.anonymize_json(value, mapping)
        return result
    
class BatchProcessor:
    """Main processor for handling rows"""
    def __init__(self, config: AnonymizationConfig, client: AnonymizationClient):
        self.config = config
        self.column_processor = ColumnProcessor(client)
        self.json_processor = JSONProcessor(client)

    def process_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize a single row of data"""
        result = row.copy()

        # do this only if standard_columns is not null
        if self.config.standard_columns is not None:
            for mapping in self.config.standard_columns:
                if mapping.column_name in result:
                    result[mapping.column_name] = self.column_processor.process_value(
                        result[mapping.column_name], 
                        mapping
                        )
                
        if self.config.json_columns is not None:
            for mapping in self.config.json_columns:
                if mapping.column_name in result:
                    result[mapping.column_name] = self.json_processor.process_value(
                        result[mapping.column_name], 
                        mapping.field_mappings
                        )
                
        return result
    
    def process_batch(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Anonymize a batch of rows of data"""
        return [self.process_row(row) for row in rows]