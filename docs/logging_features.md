# Logging Module Features

This document describes the features available in the pywrapid logging module.

## Basic Usage

```python
from pywrapid.log import setup_logging

# Setup logging with default configuration
setup_logging()

# Get a standard logger
import logging
logger = logging.getLogger(__name__)

# Log messages at different levels
logger.debug("Debug message")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```

## Structured Logging

The log module supports structured logging with automatic JSON formatting:

```python
from pywrapid.log import setup_logging, get_structured_logger

# Setup logging with structured output enabled
config = {
    "structured": {
        "enabled": True,
        "format": "json",
        "additional_fields": {
            "app_name": "MyApplication",
            "environment": "production"
        }
    }
}

setup_logging(config)
logger = get_structured_logger(__name__)

# Log with structured data
logger.info("User logged in", extra={
    "user_id": 12345,
    "ip_address": "192.168.1.1",
    "login_method": "oauth2"
})

# Output will be a JSON object like:
# {
#   "timestamp": "2025-04-17T10:30:45.123Z", 
#   "level": "INFO", 
#   "message": "User logged in", 
#   "logger": "__main__", 
#   "user_id": 12345, 
#   "ip_address": "192.168.1.1", 
#   "login_method": "oauth2", 
#   "app_name": "MyApplication", 
#   "environment": "production"
# }
```

## Cloud-Based Logging Providers

The log module includes built-in support for popular cloud logging services:

```python
from pywrapid.log import setup_logging

# Setup logging with AWS CloudWatch
config = {
    "cloud": {
        "provider": "aws_cloudwatch",
        "log_group": "my-application",
        "log_stream": "api-server",
        "aws_region": "us-east-1"
    }
}
setup_logging(config)

# Setup logging with Google Cloud Logging
config = {
    "cloud": {
        "provider": "google_cloud",
        "project_id": "my-project",
        "log_name": "application-logs",
        "credentials_path": "/path/to/credentials.json"
    }
}
setup_logging(config)
```

## Integration with Configuration Module

The logging module integrates seamlessly with the pywrapid configuration module:

```python
from pywrapid.config import WrapidConfig
from pywrapid.log import setup_logging

# Load configuration
config = WrapidConfig()
config.load("config.yml")

# Setup logging using configuration
setup_logging(config.get("logging", {}))
```

Example logging configuration in YAML:

```yaml
logging:
  level: INFO
  format: "[%(levelname)s] %(asctime)s (%(name)s) %(message)s"
  file: logs/application.log
  rotation:
    max_bytes: 10485760  # 10 MB
    backup_count: 5
  structured:
    enabled: true
    format: json
    additional_fields:
      app_name: MyApplication
      environment: development
```

## Custom Log Handlers

The log module supports custom logging handlers:

```python
import logging
from pywrapid.log import setup_logging

# Create a custom handler
class CustomHandler(logging.Handler):
    def emit(self, record):
        # Custom log processing logic
        message = self.format(record)
        # Send to custom destination
        print(f"CUSTOM: {message}")

# Register custom handler
custom_handler = CustomHandler()
custom_handler.setLevel(logging.WARNING)

# Setup logging with custom handler
config = {
    "level": "INFO",
    "custom_handlers": [custom_handler]
}
setup_logging(config)
```

## Log Filtering and Masking

The log module provides functionality for filtering sensitive data:

```python
from pywrapid.log import setup_logging, add_data_masker

# Setup logging
setup_logging()

# Add a masker for sensitive data patterns
add_data_masker(
    r"password=(\w+)", 
    replacement="password=*****"
)
add_data_masker(
    r"(\d{4}-\d{4}-\d{4}-\d{4})", 
    replacement="****-****-****-****"
)

# Logging will automatically mask sensitive data
logger = logging.getLogger(__name__)
logger.info("User data: password=secret123")  # Will log: "User data: password=*****"
logger.info("Card: 1234-5678-9012-3456")      # Will log: "Card: ****-****-****-****"
```

## Best Practices

1. **Use structured logging in production**:
   Structured logging makes it much easier to parse and analyze logs in production environments.

2. **Set appropriate log levels**:
   Use DEBUG in development, INFO or WARNING in production.

3. **Include contextual information**:
   Always include relevant context such as user IDs, request IDs, and operation details.

4. **Configure log rotation**:
   Prevent log files from growing too large by configuring rotation policies.

5. **Mask sensitive information**:
   Always mask sensitive data like passwords, tokens, and personal information.
