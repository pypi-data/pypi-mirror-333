import json
import os
from typing import Dict

import requests
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class AlohaApiError(Exception):
    """Base exception for Aloha API errors"""

    pass


class AuthenticationError(AlohaApiError):
    """Raised when authentication fails"""

    pass


class ConfigurationError(AlohaApiError):
    """Raised when required configuration is missing"""

    pass


class ApiRequestError(AlohaApiError):
    """Raised when an API request fails"""

    pass


# Set Constants
BASE_URL = os.environ.get("ALOHA_API_BASE_URL", "https://customerapi.alohaaba.com")

# Get credentials from environment variables
CLIENT_ID = os.environ.get("ALOHA_CLIENT_ID")
SECRET_KEY = os.environ.get("ALOHA_SECRET_KEY")

# Validate required credentials
if not CLIENT_ID:
    raise ConfigurationError("ALOHA_CLIENT_ID is required")
if not SECRET_KEY:
    raise ConfigurationError("ALOHA_SECRET_KEY is required")


def _redact_sensitive_data(data):
    """Redact sensitive information for logging"""
    # Skip redaction during tests
    if os.environ.get("RUNNING_TESTS") == "1":
        return data

    if not isinstance(data, dict):
        return data

    redacted = data.copy()
    if "data" in redacted:
        if isinstance(redacted["data"], dict):
            if "accessToken" in redacted["data"] and not os.environ.get("DEBUG_UNREDACT"):
                redacted["data"]["accessToken"] = redacted["data"]["accessToken"][:10] + "..."
            if "refreshToken" in redacted["data"] and not os.environ.get("DEBUG_UNREDACT"):
                redacted["data"]["refreshToken"] = redacted["data"]["refreshToken"][:10] + "..."
    return redacted


def _handle_response(response: requests.Response, operation: str) -> requests.Response:
    """Handle API response and raise appropriate exceptions"""
    try:
        if response.status_code == 401:
            raise AuthenticationError(f"{operation} failed: {response.status_code} - {response.text}")
        elif response.status_code != 200:
            raise ApiRequestError(f"{operation} failed: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"{operation} failed: {str(err)}") from err
    return response


def get_access_token() -> str:
    """Authenticate with Aloha API and return the access token."""
    url = f"{BASE_URL}/token"
    payload = json.dumps({"clientId": CLIENT_ID, "secretKey": SECRET_KEY})
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, data=payload)
        response = _handle_response(response, "Authentication")

        response_json = response.json()
        log_json = _redact_sensitive_data(response_json)
        print(f"Authentication response body: {json.dumps(log_json, indent=2)}")

        if "data" in response_json and "accessToken" in response_json["data"]:
            return response_json["data"]["accessToken"]
        else:
            raise ApiRequestError("No accessToken found in response JSON")

    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Request failed: {str(err)}") from err


def refresh_access_token(access_token: str, refresh_token: str) -> Dict:
    """Refresh an expired access token using a refresh token."""
    if not access_token or not refresh_token:
        raise ValueError("Both access_token and refresh_token are required")

    url = f"{BASE_URL}/refresh-token"
    payload = json.dumps({"clientId": CLIENT_ID, "accessToken": access_token, "refreshToken": refresh_token})
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, data=payload)
        response = _handle_response(response, "Token refresh")

        response_json = response.json()
        log_json = _redact_sensitive_data(response_json)
        print(f"Token refresh response body: {json.dumps(log_json, indent=2)}")

        return response_json

    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Request failed: {str(err)}") from err


def list_appointments(access_token: str, start_date: str, end_date: str) -> Dict:
    """Get appointments within a date range."""
    if not all([access_token, start_date, end_date]):
        raise ValueError("access_token, start_date, and end_date are required")

    url = f"{BASE_URL}/v1/report/appointments?startDate={start_date}&endDate={end_date}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url=url, headers=headers)
        response_json = _handle_response(response, "List appointments").json()
        return response_json

    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Failed to list appointments: {str(err)}") from err


def list_clients(access_token: str) -> Dict:
    """
    Get list of all clients.

    Args:
        access_token (str): Authentication token from get_access_token()

    Returns:
        dict: The API response data containing clients

    Raises:
        AuthenticationError: If the access token is invalid
        ApiRequestError: If the API request fails
    """
    if not access_token:
        raise ValueError("access_token is required")

    url = f"{BASE_URL}/v1/report/clients"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url=url, headers=headers)
        return _handle_response(response, "List clients").json()
    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Failed to list clients: {str(err)}") from err


def list_authorizations(access_token: str, start_date: str, end_date: str) -> Dict:
    """
    Get authorizations within a date range.

    Args:
        access_token (str): Authentication token from get_access_token()
        start_date (str): Start date in format YYYY-MM-DD
        end_date (str): End date in format YYYY-MM-DD

    Returns:
        dict: The API response data containing authorizations

    Raises:
        AuthenticationError: If the access token is invalid
        ApiRequestError: If the API request fails
        ValueError: If start_date or end_date are invalid
    """
    if not all([access_token, start_date, end_date]):
        raise ValueError("access_token, start_date, and end_date are required")

    url = f"{BASE_URL}/v1/report/client-authorizations?startDate={start_date}&endDate={end_date}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url=url, headers=headers)
        return _handle_response(response, "List authorizations").json()
    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Failed to list authorizations: {str(err)}") from err


def list_billing_ledger(access_token: str, start_date: str, end_date: str) -> Dict:
    """
    Get billing ledger data within a date range.

    This endpoint generates a summary report of claims paid by payers, including
    primary and secondary payers. It details co-pays, co-insurance, deductibles,
    and any adjustments made.

    Args:
        access_token (str): Authentication token from get_access_token()
        start_date (str): Start date in format YYYY-MM-DD
        end_date (str): End date in format YYYY-MM-DD

    Returns:
        dict: The API response data containing billing ledger entries

    Raises:
        AuthenticationError: If the access token is invalid
        ApiRequestError: If the API request fails
        ValueError: If start_date or end_date are invalid
    """
    if not all([access_token, start_date, end_date]):
        raise ValueError("access_token, start_date, and end_date are required")

    url = f"{BASE_URL}/v1/report/billing-ledger?startDate={start_date}&endDate={end_date}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url=url, headers=headers)
        response_json = _handle_response(response, "List billing ledger").json()
        return response_json

    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Failed to list billing ledger: {str(err)}") from err


def list_authorizations_without_appointments(access_token: str, start_date: str, end_date: str) -> Dict:
    """
    Get authorizations without scheduled appointments within a date range.

    This endpoint helps identify client authorizations that don't have any
    appointments scheduled, which is useful for ensuring that authorized
    services are being utilized properly.

    Args:
        access_token (str): Authentication token from get_access_token()
        start_date (str): Start date in format YYYY-MM-DD
        end_date (str): End date in format YYYY-MM-DD

    Returns:
        dict: The API response data containing authorizations without appointments

    Raises:
        AuthenticationError: If the access token is invalid
        ApiRequestError: If the API request fails
        ValueError: If start_date or end_date are invalid
    """
    if not all([access_token, start_date, end_date]):
        raise ValueError("access_token, start_date, and end_date are required")

    url = f"{BASE_URL}/v1/report/authorizations-without-appointments?startDate={start_date}&endDate={end_date}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url=url, headers=headers)
        response_json = _handle_response(response, "List authorizations without appointments").json()
        return response_json

    except requests.exceptions.RequestException as err:
        raise ApiRequestError(f"Failed to list authorizations without appointments: {str(err)}") from err
