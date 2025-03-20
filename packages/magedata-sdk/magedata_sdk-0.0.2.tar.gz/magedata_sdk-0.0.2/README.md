# Anonymization SDK User Guide

## Overview

The Mage Data Anonymization SDK provides a flexible and powerful way to anonymize sensitive data in various formats, including structured columns and JSON fields. The SDK is designed to work with any data source that can provide dictionary-like records, such as databases, CSV files, or JSON documents.

## License

This software uis proprietary and is licensed under the terms of our Proprietary Software License agreement. All rights reserved. Unauthorized copying, distribution, or use is strictly prohibited.

Contact Mage Data at support at magedata dot ai for licensing inquiries.

## Installation

```bash
pip install magedata_sdk
```

## Configuration

The SDK uses two separate configuration files:

1. **Client Configuration** - Contains API connection settings
2. **Anonymization Configuration** - Contains data mapping and PII rules

### Client Configuration

The client configuration contains the settings needed to connect to the anonymization service API:

```json
{
  "base_url": "https://api.anonymization-service.com",
  "api_key": "env:ANONYMIZATION_API_KEY",
  "anon_api_port": 8088,
  "analyze_api_port": 8089,
  "anonymize_api_port": 8090,
  "timeout": 30,
  "retries": 3,
  "retry_delay": 1
}
```

**Security Note**: For sensitive values like API keys, use the `env:` prefix to load from environment variables.

### Anonymization Configuration

The anonymization configuration defines how your data should be processed:

```json
{
  "standard_columns": [
    {
      "column_name": "email",
      "dc_types": [ "Email Addresses" ],
      "mapping_type": "simple"
    },
    {
      "column_name": "phone_number",
      "dc_types": [ "Phone" ],
      "mapping_type": "simple"
    }
  ],
  "json_columns": [
    {
      "column_name": "user_profile",
      "field_mappings": [
        {
          "jsonpath": "$.name",
          "mapping_type": "simple",
          "dc_types": [ "Full Name" ]
        },
        {
          "jsonpath": "$.contact_info",
          "mapping_type": "description",
          "dc_types": ["Phone", "Email Addresses", "Address"]
        }
      ]
    }
  ],
  "global_parameters": {
    "language": "en-US"
  }
}
```

## Basic Usage

### 1. Loading Configurations

```python
from magedata_sdk import ConfigurationManager

# Load configurations
client_config = ConfigurationManager.load_client_config("client_config.json")
anonymization_config = ConfigurationManager.load_anonymization_config("anonymization_config.json")
```

### 2. Setting Up the Client and Processor

```python
from magedata_sdk import AnonymizationClient, BatchProcessor

# Initialize client
client = AnonymizationClient(
    base_url=client_config.base_url,
    anon_api_port=client_config.anon_api_port,
    analyze_api_port=client_config.analyze_api_port,
    anonymize_api_port=client_config.anonymize_api_port,
    api_key=client_config.api_key,
    timeout=client_config.timeout,
    retries=client_config.retries
)

# Create processor
processor = BatchProcessor(anonymization_config, client)
```

### 3. Processing Data

```python
# Example data
data = [
    {
        "email": "john.doe@example.com",
        "phone_number": "555-0123",
        "user_profile": {
            "name": "John Doe",
            "contact_info": "Call John at 555-0123 or email john.doe@example.com"
        }
    }
]

# Process data
try:
    anonymized_data = processor.process_batch(data)
    print(anonymized_data)
except Exception as e:
    print(f"Processing failed: {str(e)}")
```

## Advanced Usage

### Processing Database Results

```python
import sqlite3
from magedata_sdk import ConfigurationManager, AnonymizationClient, BatchProcessor

# Set up configuration and processor
client_config = ConfigurationManager.load_client_config("client_config.json")
anonymization_config = ConfigurationManager.load_anonymization_config("anonymization_config.json")

client = AnonymizationClient(
    base_url=client_config.base_url,
    api_key=client_config.api_key
)
processor = BatchProcessor(anonymization_config, client)

# Connect to database and fetch data
conn = sqlite3.connect("your_database.db")
conn.row_factory = sqlite3.Row  # This returns rows as dictionaries
cursor = conn.cursor()
cursor.execute("SELECT email, phone, profile_json FROM users LIMIT 100")
rows = cursor.fetchall()

# Convert rows to list of dictionaries
data = []
for row in rows:
    # Parse JSON fields if needed
    item = dict(row)
    if 'profile_json' in item and item['profile_json']:
        item['profile_json'] = json.loads(item['profile_json'])
    data.append(item)

# Process data
anonymized_data = processor.process_batch(data)

# Now you can use anonymized_data
# For example, write it back to another table
```

### Processing JSON Files

```python
import json
from magedata_sdk import ConfigurationManager, AnonymizationClient, BatchProcessor

# Set up configuration and processor
client_config = ConfigurationManager.load_client_config("client_config.json")
anonymization_config = ConfigurationManager.load_anonymization_config("anonymization_config.json")

client = AnonymizationClient(
    base_url=client_config.base_url,
    api_key=client_config.api_key
)
processor = BatchProcessor(anonymization_config, client)

# Read JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Process data
anonymized_data = processor.process_batch(data)

# Write anonymized data to file
with open("anonymized_data.json", "w") as f:
    json.dump(anonymized_data, f, indent=2)
```

### Processing CSV Files

```python
import csv
import json
from magedata_sdk import ConfigurationManager, AnonymizationClient, BatchProcessor

# Set up configuration and processor
client_config = ConfigurationManager.load_client_config("client_config.json")
anonymization_config = ConfigurationManager.load_anonymization_config("anonymization_config.json")

client = AnonymizationClient(
    base_url=client_config.base_url,
    api_key=client_config.api_key
)
processor = BatchProcessor(anonymization_config, client)

# Read CSV file
data = []
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Parse JSON columns if necessary
        if 'user_data' in row and row['user_data']:
            try:
                row['user_data'] = json.loads(row['user_data'])
            except:
                # Handle invalid JSON
                row['user_data'] = {}
        data.append(row)

# Process data
anonymized_data = processor.process_batch(data)

# Write anonymized data to file
with open("anonymized_data.csv", "w") as f:
    if data:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in anonymized_data:
            # Convert JSON fields back to strings
            for field in row:
                if isinstance(row[field], dict):
                    row[field] = json.dumps(row[field])
            writer.writerow(row)
```

### Batch Processing

For large datasets, process in batches to avoid memory issues:

```python
BATCH_SIZE = 1000
results = []

for i in range(0, len(data), BATCH_SIZE):
    batch = data[i:i+BATCH_SIZE]
    batch_results = processor.process_batch(batch)
    results.extend(batch_results)
```

## Error Handling

Implement proper error handling for production use:

```python
from magedata_sdk.exceptions import AnonymizationError, APIError, ConfigurationError

try:
    anonymized_data = processor.process_batch(data)
except APIError as e:
    logger.error(f"API error: {str(e)}")
    # Handle API issues (retry, alert, etc.)
except ConfigurationError as e:
    logger.error(f"Configuration error: {str(e)}")
    # Handle configuration issues
except AnonymizationError as e:
    logger.error(f"Anonymization error: {str(e)}")
    # Handle general anonymization issues
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    # Handle unexpected errors
```

## Security Best Practices

1. **API Key Management**
   - Use environment variables for API keys
   - Rotate keys regularly
   - Use different keys for different environments

2. **Data Handling**
   - Avoid storing original and anonymized data together
   - Implement proper access controls
   - Clear sensitive data from memory after processing

3. **Configuration Security**
   - Validate configurations before use
   - Implement RBAC for configuration management
   - Audit configuration changes

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check base URL and network connectivity
   - Verify API key is correct and active
   - Check firewall settings

2. **Configuration Errors**
   - Validate JSON syntax
   - Check for required fields
   - Verify JSON paths are valid

3. **Processing Errors**
   - Check data structure matches configuration
   - Verify JSON columns contain valid JSON
   - Ensure all referenced columns exist

### Logging

Enable detailed logging for troubleshooting:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='anonymization.log'
)
```

## Support

For assistance with the SDK:
- Submit issues on GitHub
- Contact support at support@magedata.ai
- Refer to the API documentation