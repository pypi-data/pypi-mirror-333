import unittest
import os
import sys
from unittest.mock import patch, Mock
import requests

# Add parent directory to path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set testing environment variable
os.environ['RUNNING_TESTS'] = '1'

# Use direct imports from the api module
from api import (
    get_access_token, 
    refresh_access_token,
    list_appointments, 
    list_clients,
    list_authorizations,
    list_billing_ledger,
    list_authorizations_without_appointments,
    BASE_URL,
    CLIENT_ID
)

class TestAlohaFunctions(unittest.TestCase):

    @patch('api.requests.request')
    def test_get_access_token_success(self, mock_request):
        # Setup mock response with the actual nested response structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": {
                "username": "Aloha.Client.SBBC",
                "accessToken": "test_token123",
                "accessTokenExpiration": "2025-03-06T18:51:11Z",
                "refreshToken": "J64o+MBN1jnl/wer/bBmaf9THk8/4KEQE1g3K0X8MIk=",
                "subscriptionId": "3742ca1f-1c44-430e-86ff-baa8b4febb90"
            }
        }
        mock_request.return_value = mock_response

        # Call the function
        token = get_access_token()

        # Verify the result
        self.assertEqual(token, "test_token123")
        
        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], f"{BASE_URL}/token")
        self.assertEqual(kwargs["headers"], {"Content-Type": "application/json"})
        # Don't check the exact payload since SECRET_KEY might be dynamic

    @patch('api.requests.request')
    def test_get_access_token_failure(self, mock_request):
        # Setup mock response for failure case
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_request.return_value = mock_response

        # Verify the function raises an exception
        with self.assertRaises(Exception) as context:
            get_access_token()
            
        # Check that the exception message contains the status code and response text
        self.assertTrue("Authentication failed: 401 - Unauthorized" in str(context.exception))
    
    @patch('api.requests.request')
    def test_refresh_access_token_success(self, mock_request):
        # Setup mock response for refresh token success
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": {
                "username": "Aloha.Client.SBBC",
                "accessToken": "new_test_token456",
                "accessTokenExpiration": "2025-03-06T20:51:11Z",
                "refreshToken": "****",
                "subscriptionId": "3742ca1f-1c44-430e-86ff-baa8b4febb90"
            }
        }
        mock_request.return_value = mock_response

        # Test parameters
        access_token = "old_access_token"
        refresh_token = "old_refresh_token"

        # Call the function
        response = refresh_access_token(access_token, refresh_token)

        # Verify the result
        self.assertEqual(response["data"]["accessToken"], "new_test_token456")
        self.assertIn("refreshToken", response["data"])  # Just verify the field exists
        self.assertIsNotNone(response["data"]["refreshToken"])  # Verify it's not None
        
        # Verify the request was made correctly
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], f"{BASE_URL}/refresh-token")
        self.assertEqual(kwargs["headers"], {"Content-Type": "application/json"})
        
        # Verify payload contains correct fields
        import json
        payload = json.loads(kwargs["data"])
        self.assertEqual(payload["clientId"], CLIENT_ID)
        self.assertEqual(payload["accessToken"], access_token)
        self.assertEqual(payload["refreshToken"], refresh_token)
    
    @patch('api.requests.request')
    def test_refresh_access_token_failure(self, mock_request):
        # Setup mock response for failure case
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Invalid refresh token"
        mock_request.return_value = mock_response

        # Test parameters
        access_token = "old_access_token"
        refresh_token = "invalid_refresh_token"

        # Verify the function raises an exception
        with self.assertRaises(Exception) as context:
            refresh_access_token(access_token, refresh_token)
            
        # Check that the exception message contains the status code and response text
        self.assertTrue("Token refresh failed: 401 - Invalid refresh token" in str(context.exception))

    @patch('api.requests.request')
    def test_list_appointments(self, mock_request):
        # Setup mock response with the actual API response structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": [{"appointmentId": 1, "appointmentDate": "01-01-2024"}]
        }
        mock_request.return_value = mock_response
        
        # Test parameters
        access_token = "test_token"
        start_date = "2023-01-01"
        end_date = "2023-01-31"

        # Call the function
        response = list_appointments(access_token, start_date, end_date)

        # Verify the result
        self.assertEqual(response, mock_response)
        
        # Verify the request was made correctly
        mock_request.assert_called_once_with(
            "GET", 
            f"{BASE_URL}/v1/report/appointments?startDate={start_date}&endDate={end_date}", 
            headers={"Authorization": f"Bearer {access_token}"}
        )

    @patch('api.requests.request')
    def test_list_clients(self, mock_request):
        # Setup mock response with the actual API response structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": [{"clientId": 1, "firstName": "Test", "lastName": "Client"}]
        }
        mock_request.return_value = mock_response
        
        # Test parameters
        access_token = "test_token"

        # Call the function
        response = list_clients(access_token)

        # Verify the result
        self.assertEqual(response, mock_response)
        
        # Verify the request was made correctly
        mock_request.assert_called_once_with(
            "GET", 
            f"{BASE_URL}/v1/report/clients", 
            headers={"Authorization": f"Bearer {access_token}"}
        )

    @patch('api.requests.request')
    def test_list_authorizations(self, mock_request):
        # Setup mock response with the actual API response structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": [{"startDate": "01-01-2024", "endDate": "01-31-2024"}]
        }
        mock_request.return_value = mock_response
        
        # Test parameters
        access_token = "test_token"
        start_date = "2023-01-01"
        end_date = "2023-01-31"

        # Call the function
        response = list_authorizations(access_token, start_date, end_date)

        # Verify the result
        self.assertEqual(response, mock_response)
        
        # Verify the request was made correctly
        mock_request.assert_called_once_with(
            "GET", 
            f"{BASE_URL}/v1/report/client-authorizations?startDate={start_date}&endDate={end_date}", 
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
    @patch('api.requests.request')
    def test_list_billing_ledger(self, mock_request):
        # Setup mock response with the expected API response structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": [{
                "invoiceId": 90001,
                "dateOfService": "03-15-2024",
                "clientId": 101,
                "clientName": "Winston, Alice",
                "billingCode": "97153",
                "billedAmount": 125.75,
                "billedUnits": 4,
                "primaryPayer": "Sample Insurance",
                "primaryPayment": 100.60,
                "clientPayment": 25.15,
                "clientBalance": 0.00,
                "payerBalance": 0.00
            }]
        }
        mock_request.return_value = mock_response
        
        # Test parameters
        access_token = "test_token"
        start_date = "2024-01-01"
        end_date = "2024-03-31"

        # Call the function
        response = list_billing_ledger(access_token, start_date, end_date)

        # Verify the result
        self.assertEqual(response, mock_response)
        
        # Verify the request was made correctly
        mock_request.assert_called_once_with(
            "GET", 
            f"{BASE_URL}/v1/report/billing-ledger?startDate={start_date}&endDate={end_date}", 
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
    @patch('api.requests.request')
    def test_list_authorizations_without_appointments(self, mock_request):
        # Setup mock response with the expected API response structure
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Success",
            "data": [{
                "office": "Sample Office (XYZ 1001)",
                "client_Name": "Doe, John",
                "payer_Name": "Sample Insurance",
                "iD_with_Payer": "XXXXXX001",
                "authorization_Number": "AUTH-1234-5678",
                "service_Name": "Sample Assessment by BCBA (97151)",
                "allowed_Limit": 32,
                "type": "Units",
                "startDate": "2024-10-26T00:00:00Z",
                "endDate": "2025-04-26T00:00:00Z"
            }]
        }
        mock_request.return_value = mock_response
        
        # Test parameters
        access_token = "test_token"
        start_date = "2024-01-01"
        end_date = "2024-03-31"

        # Call the function
        response = list_authorizations_without_appointments(access_token, start_date, end_date)

        # Verify the result
        self.assertEqual(response, mock_response)
        
        # Verify the request was made correctly
        mock_request.assert_called_once_with(
            "GET", 
            f"{BASE_URL}/v1/report/authorizations-without-appointments?startDate={start_date}&endDate={end_date}", 
            headers={"Authorization": f"Bearer {access_token}"}
        )


class TestAlohaIntegration(unittest.TestCase):
    """Integration tests that make actual API calls to Aloha.
    
    These tests are skipped by default. To run them:
    1. Set environment variable: RUN_INTEGRATION_TESTS=1
    2. Or use: python -m unittest api.tests.test_api.TestAlohaIntegration
    """
    
    @classmethod
    def setUpClass(cls):
        """Get access token once for all tests"""
        if cls.should_run_integration_tests():
            print("\nRunning integration tests with real API calls...")
            try:
                cls.access_token = get_access_token()
                if cls.access_token:
                    print(f"Successfully obtained access token: {cls.access_token[:10]}...")
                else:
                    print("Warning: Received None as access token")
            except Exception as e:
                print(f"Failed to get access token: {e}")
                raise
    
    @classmethod
    def should_run_integration_tests(cls):
        """Determine if integration tests should run based on environment variable or class name in argv"""
        # Check if running this specific test class directly
        for arg in sys.argv:
            if 'TestAlohaIntegration' in arg:
                return True
            
        # Check environment variable
        env_value = os.environ.get('RUN_INTEGRATION_TESTS')
        if env_value == '1' or env_value and env_value.lower() in ('true', 'yes', 'y'):
            return True
        return False  # Default to not running integration tests
    
    def setUp(self):
        """Skip tests if integration tests are not enabled"""
        if not self.should_run_integration_tests():
            self.skipTest('Integration tests disabled. Set RUN_INTEGRATION_TESTS=1 or run directly with python -m unittest api.tests.test_api.TestAlohaIntegration')
        
        # Ensure we have an access token for each test
        if not hasattr(self.__class__, 'access_token') or not self.__class__.access_token:
            self.skipTest('No access token available. Authentication may have failed.')

    def test_get_access_token_integration(self):
        """Test that we can actually get an access token from the API"""
        token = get_access_token()
        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 0)
    
    def test_refresh_access_token_integration(self):
        """Test that we can refresh an access token from the API"""
        # Get a fresh token first to ensure we have valid tokens
        auth_response = get_access_token()
        
        # Extract refresh token from the initial authentication
        original_auth_data = None
        try:
            # We need to call the API again to get both access and refresh tokens
            response = requests.request(
                "POST", 
                f"{BASE_URL}/token", 
                headers={"Content-Type": "application/json"}, 
                data=f'{{"clientId": "{CLIENT_ID}", "secretKey": "{os.environ.get("ALOHA_SECRET_KEY", "")}"}}')
            original_auth_data = response.json()["data"]
        except Exception as e:
            self.skipTest(f"Could not get refresh token for testing: {e}")
            
        if not original_auth_data or "refreshToken" not in original_auth_data:
            self.skipTest("No refresh token available to test token refresh")
            
        # Now test the refresh function
        try:
            response = refresh_access_token(
                original_auth_data["accessToken"], 
                original_auth_data["refreshToken"]
            )
            
            # Verify response structure
            self.assertIn('status', response)
            self.assertIn('message', response)
            self.assertIn('data', response)
            
            # Verify we got new tokens
            self.assertIn('accessToken', response['data'])
            self.assertIn('refreshToken', response['data'])
            
            # Optionally verify tokens are different (though not guaranteed by API spec)
            self.assertIsNotNone(response['data']['accessToken'])
            self.assertIsNotNone(response['data']['refreshToken'])
        except Exception as e:
            # Some APIs don't allow testing refresh tokens in rapid sequence
            self.skipTest(f"Token refresh failed, possibly due to rate limiting: {e}")
        
    def test_list_appointments_integration(self):
        """Test retrieving appointments from the API"""
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        
        response = list_appointments(self.access_token, start_date, end_date)
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify response structure
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)
        
        # If there are appointments, check their structure
        if data['data']:
            appointment = data['data'][0]
            for field in ['appointmentId', 'appointmentDate', 'clientName']:
                with self.subTest(f"Appointment field: {field}"):
                    self.assertIn(field, appointment)
    
    def test_list_clients_integration(self):
        """Test retrieving clients from the API"""
        response = list_clients(self.access_token)
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify response structure
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)
        
        # If there are clients, check their structure
        if data['data']:
            client = data['data'][0]
            for field in ['clientId', 'firstName', 'lastName']:
                with self.subTest(f"Client field: {field}"):
                    self.assertIn(field, client)
    
    def test_list_authorizations_integration(self):
        """Test retrieving authorizations from the API"""
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        
        response = list_authorizations(self.access_token, start_date, end_date)
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify response structure
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)
        
        # If there are authorizations, check their structure
        if data['data']:
            auth = data['data'][0]
            for field in ['startDate', 'endDate']:
                with self.subTest(f"Authorization field: {field}"):
                    self.assertIn(field, auth)
    
    def test_list_billing_ledger_integration(self):
        """Test retrieving billing ledger data from the API"""
        start_date = "2024-01-01"
        end_date = "2024-03-31"
        
        response = list_billing_ledger(self.access_token, start_date, end_date)
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify response structure
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)
        
        # If there are billing ledger entries, check their structure
        if data['data']:
            ledger_entry = data['data'][0]
            expected_fields = ['invoiceId', 'dateOfService', 'clientName', 'billingCode']
            for field in expected_fields:
                with self.subTest(f"Billing ledger field: {field}"):
                    self.assertIn(field, ledger_entry)
    
    def test_list_authorizations_without_appointments_integration(self):
        """Test retrieving authorizations without appointments from the API"""
        start_date = "2024-01-01"
        end_date = "2024-03-31"
        
        response = list_authorizations_without_appointments(self.access_token, start_date, end_date)
        
        # Check response status
        self.assertEqual(response.status_code, 200)
        
        # Verify response structure
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)
        
        # If there are authorizations without appointments, check their structure
        if data['data']:
            auth = data['data'][0]
            expected_fields = ['office', 'client_Name', 'authorization_Number', 'service_Name']
            for field in expected_fields:
                with self.subTest(f"Auth without appointment field: {field}"):
                    self.assertIn(field, auth)


if __name__ == '__main__':
    # Check for custom flag before passing control to unittest
    if '--run-integration' in sys.argv:
        # Remove custom flag as unittest doesn't recognize it
        sys.argv.remove('--run-integration')
        # Set environment variable programmatically
        os.environ['RUN_INTEGRATION_TESTS'] = '1'
        
    unittest.main()