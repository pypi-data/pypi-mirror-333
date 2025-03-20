# Copyright (c) 2025 Mage Data. All Rights Reserved.
# This file is part of Mage Data SDK, which is licensed under a proprietary license.
# See the LICENSE file in the package root for license terms.

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class MappingType(Enum):
    SIMPLE = "simple"
    DESCRIPTIVE = "descriptive"
    JSON = "json"

class DCType(Enum):
    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    FULL_NAME = "Full Name"
    EMAIL_ADDRESS = "Email Addresses"
    PHONE_NUMBER = "Phone"
    CREDIT_CARD = "Credit Card Information"
    DATE_OF_BIRTH = "Date of Birth"
    ADDRESS = "Address"
    NATIONAL_IDENTIFIER = "National Identifier"
    CITY = "City"


class ColumnAttributes(BaseModel):
    mapping_type: MappingType = Field(MappingType.SIMPLE)
    dc_types: List[DCType]
    parameters: Optional[Dict[str, Any]] = None

class ColumnMapping(ColumnAttributes):
    """Configuration for Column Anonymization"""
    column_name: str

class JSONFieldMapping(ColumnAttributes):
    """Configuration for JSON field Anonymization. Only the JSON Path will be defined in addition to the column mapping"""
    json_path: str
    
    #mapping_type: MappingType
    #dc_type: DCType
    #detect_categories: Optional[List[DCType]] = None
    #parameters: Optional[Dict[str, Any]] = None

class JSONColumnMapping(BaseModel):
    """Configuration for JSON column Mapping"""
    column_name: str
    field_mappings: List[JSONFieldMapping]

class AnonymizationConfig(BaseModel):
    """Complete Template for anonymization"""
    standard_columns: List[ColumnMapping] = None
    json_columns: List[JSONColumnMapping] = None
    global_parameters: Optional[Dict[str, Any]] = None