# Aloha API Client

A Python client for interacting with the Aloha ABA Practice Management Software API.

## Installation

```bash
pip install aloha_api
```

## Usage

```python
import os
from aloha_api import get_access_token, list_clients

# Set your credentials as environment variables
os.environ["ALOHA_CLIENT_ID"] = "your_client_id"
os.environ["ALOHA_SECRET_KEY"] = "your_secret_key"

# Get an access token
token = get_access_token()

# Fetch client data
response = list_clients(token)
clients = response.json()["data"]
print(clients)
```

## Available Functions

- `get_access_token()`: Authenticate and get an access token
- `refresh_access_token(access_token, refresh_token)`: Refresh an expired token
- `list_clients(access_token)`: Get a list of all clients
- `list_appointments(access_token, start_date, end_date)`: Get appointments for a date range
- `list_authorizations(access_token, start_date, end_date)`: Get authorizations for a date range
- `list_billing_ledger(access_token, start_date, end_date)`: Get billing data for a date range
- `list_authorizations_without_appointments(access_token, start_date, end_date)`: Find unused authorizations

## Documentation

See vendor-doc.md for complete API documentation.
