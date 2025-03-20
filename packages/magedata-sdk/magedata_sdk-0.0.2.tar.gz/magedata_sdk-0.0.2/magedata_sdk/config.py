# Copyright (c) 2025 Mage Data. All Rights Reserved.
# This file is part of Mage Data SDK, which is licensed under a proprietary license.
# See the LICENSE file in the package root for license terms.

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from .models import AnonymizationConfig
from .exceptions import ConfigurationError

class ClientConfig(BaseModel):
    """API Client Configuration"""

    """
    Should not need the port numbers once API gateway has been implemented
    """
    base_url: str     
    anon_api_port: int
    analyze_api_port: int
    anonymize_api_port: int
    api_key: str = Field(default="")
    timeout: int = 30
    retries: int = 3
    retry_delay: int = 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientConfig":
        """Create from dictionary with environment variable support"""
        if "api_key" in data and data["api_key"].startswith("env:"):
            env_var = data["api_key"].split(":",1)[1]
            if env_var in os.environ:
                data["api_key"] = os.environ[env_var]

        return cls(**data)

class ConfigurationManager:
    """Manages the configurations for the anonymization client and template"""

    @staticmethod
    def load_anonymization_config(filepath: str) -> AnonymizationConfig:
        """
        Load anonymization configuration from a json file
        """
        try:
            with open(filepath, 'r') as f:
                config_data = json.load(f)
            return AnonymizationConfig(**config_data)
        except Exception as e:
            raise ConfigurationError(f"Error loading anonymization configuration: {e}")
        
    @staticmethod
    def load_client_config(filepath: str) -> ClientConfig:
        """
        Load client configuration from a json file
        """
        try:
            with open(filepath, 'r') as f:
                config_data = json.load(f)
            return ClientConfig.from_dict(config_data)
        except Exception as e:
            raise ConfigurationError(f"Error loading client configuration: {e}")