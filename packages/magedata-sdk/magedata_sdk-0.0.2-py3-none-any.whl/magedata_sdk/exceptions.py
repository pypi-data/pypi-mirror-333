# Copyright (c) 2025 Mage Data. All Rights Reserved.
# This file is part of Mage Data SDK, which is licensed under a proprietary license.
# See the LICENSE file in the package root for license terms.

class AnonymizationError(Exception):
    """Base exception for anonymization errors"""
    pass

class APIError(AnonymizationError):
    """Base exception for API errors"""
    pass

class ConfigurationError(AnonymizationError):
    """Base exception for configuration errors"""
    pass

class ValidationError(AnonymizationError):
    """Base exception for data validation errors"""
    pass
