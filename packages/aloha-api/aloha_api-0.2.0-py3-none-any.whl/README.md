# Aloha API Client

A Python client for the Aloha ABA Practice Management Software API.
 

[![Python package](https://github.com/jhaisley/aloha_api/actions/workflows/python-package.yml/badge.svg)](https://github.com/jhaisley/aloha_api/actions/workflows/python-package.yml)
[![PyPi Package](https://github.com/jhaisley/aloha_api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jhaisley/aloha_api/actions/workflows/python-publish.yml)

## Installation

```bash
pip install aloha_api
```

## Configuration

The client requires the following environment variables to be set:

- `ALOHA_CLIENT_ID`: Your Aloha API client ID
- `ALOHA_SECRET_KEY`: Your Aloha API secret key
- `ALOHA_API_BASE_URL`: (Optional) API base URL, defaults to https://customerapi.alohaaba.com

You can set these either in your environment or in a `.env` file. A template is provided in `.env.template`.

## Usage

```python
from aloha_api import get_access_token, list_clients

# Get an access token
token = get_access_token()

# List all clients
clients = list_clients(token)
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

## Development

### Setting up the development environment

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.template` to `.env` and fill in your credentials:
   ```bash
   cp .env.template .env
   ```

### Running Tests

The test suite includes both unit tests and integration tests.

#### Unit Tests
Run unit tests with:
```bash
pytest
```

#### Integration Tests
Integration tests make real API calls and require valid credentials.

To run integration tests:

1. Configure your `.env` file with valid credentials
2. Enable integration tests by setting `RUN_INTEGRATION_TESTS=1` in your `.env`
3. Run the tests:
   ```bash
   # Run all tests including integration
   pytest
   
   # Run only integration tests
   pytest -v -k "Integration"
   
   # Run specific integration test class
   python -m unittest tests.test_api.TestAlohaIntegration
   ```

### Code Style
This project uses `ruff` for code formatting and linting:

```bash
# Format code
ruff format .

# Check style
ruff check .
```

## Documentation

See vendor-doc.md or https://api-docs.alohaaba.com for complete API documentation.
