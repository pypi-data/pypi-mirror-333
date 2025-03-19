# Aloha Customer API Documentation

## Overview

The Aloha Customer API allows you to programmatically access data stored in Aloha Practice Management Software with ease.

1. You need a valid `clientId` and `secretKey` to generate a short-lived `bearer access_token` which will be required to send requests to the API endpoints.

2. The API has an access rate limit applied to it.

3. The API will only respond to secured communication done over HTTPS. HTTP requests will be sent a `301` redirect to corresponding HTTPS resources.

4. The API supports only TLS 1.3 and TLS 1.2 protocols for secure communication. It is recommended to use TLS 1.3 as it is faster and more secure.

5. It is recommended to use HTTP/2 (h2) ALPN over HTTP/1.1 as it provides better performance and efficiency.

6. The API is versioned. Include the version in your endpoint paths, e.g., `/v1/resource`.

7. Response to every request is sent in JSON format. In case the API request results in an error, it is represented by an `"errors": {}` key in the JSON response.

8. The request method (verb) determines the nature of action you intend to perform. A request made using the `GET` method implies that you want to fetch something from the API, `PUT` implies that you want to add something new to the API, `POST` implies that you want to update something to the API and `DELETE` implies that you want to delete something from the API.

9. The API calls will respond with appropriate HTTP status codes for all requests.

## Authentication

Valid `bearer access_token` is required to be sent as part of every request to the Aloha Customer API, in the form of an `Authorization` request header. You need to generate `access_token` by calling **Generate AccessToken** endpoint. The `bearer access_token` are short-lived and requiring refresh every 3 hours from the generation time.

## Authentication Endpoints

### Generate AccessToken

```
POST https://customerapi.alohaaba.com/token
```

This endpoint allows the client to obtain an `access_token` by providing the client ID and secret key.

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| clientId | string | The client ID of the requester |
| secretKey | string | The secret key for authentication |

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| username | string | The username associated with the token |
| accessToken | string | The access token for authentication |
| accessTokenExpiration | string | The expiration date of the access token |
| refreshToken | string | The refresh token for obtaining a new access token |
| subscriptionId | string | The ID of the subscription |

### Refresh AccessToken

```
POST https://customerapi.alohaaba.com/refresh-token
```

This endpoint is used to refresh the access token using a refresh token.

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| clientId | string | The client ID of the requester |
| accessToken | string | The current access token |
| refreshToken | string | The refresh token for obtaining a new access token |

#### Response Fields

Same as Generate AccessToken response.

## Error Codes

| Header | Description |
|--------|-------------|
| `400` | A validation error had occurred |
| `401` | A not authenticated error had occurred |
| `403` | A not authorized error had occurred |
| `404` | A path not found or primary entity not found |
| `429` | Rate limit exceeded, or you are not hitting the correct URL. Please refer to the error message that came with the code. |
| `500` | An internal error has occurred, this is probably not your fault. |

## Rate Limits

API access rate limits are applied at a per-key basis in unit time. Access to the API using a key is limited to **1,000 requests** per day. In addition, every API response is accompanied by the following set of headers to identify the status of your consumption.

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | The maximum number of requests that the consumer is permitted to make per day. |
| `X-RateLimit-Remaining` | The number of requests remaining in the current rate limit window. |
| `X-RateLimit-Reset` | The time at which the current rate limit window resets in UTC epoch seconds. |

Once you hit the rate limit, you will receive a response similar to the following JSON, with a status code of `429 Too Many Requests`.

```json
{
 "status": 429,
 "message": "Too Many Requests",
 "errors": [
 {
 "name": "RateLimitError",
 "message": "Rate Limit exceeded. Please retry at 1716595200"
 }
 ]
}
```

## API Endpoints

### 1. List Client Authorizations

```
GET https://customerapi.alohaaba.com/v1/report/client-authorizations
```

Retrieves client authorizations within a specified date range.

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| startDate | query | Start date in YYYY-MM-DD format |
| endDate | query | End date in YYYY-MM-DD format |


### 2. List Billing Ledger

```
GET https://customerapi.alohaaba.com/v1/report/billing-ledger
```

Retrieves billing ledger data within a date range.

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| startDate | query | Start date in YYYY-MM-DD format |
| endDate | query | End date in YYYY-MM-DD format |

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| status | integer | Response status code |
| message | string | Additional information or error messages |
| data | array | Array of billing ledger entries |

##### Billing Ledger Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| invoiceId | integer | Unique identifier for the invoice |
| dateOfService | string | Service date in mm-dd-yyyy format |
| clientId | integer | Unique identifier for the client |
| clientName | string | Name of the client |
| office | string | Name of the office |
| billingCode | string | Billing code for the service |
| modifiers | string | Any modifiers applied to the billing code |
| placeOfService | integer | Place of service code |
| billedAmount | number | Total amount billed |
| billedUnits | integer | Number of units billed |
| contractAmount | number | Contracted amount |
| primaryPayer | string | Primary insurance payer |
| primaryPayment | number | Payment from primary payer |
| clientPayment | number | Payment from client |
| clientBalance | number | Remaining client balance |
| payerBalance | number | Remaining payer balance |
| adjustments | number | Any adjustments |
| renderingProvider | string | Provider who rendered the service |

### 3. Authorizations Without Appointments

```
GET https://customerapi.alohaaba.com/v1/report/authorizations-without-appointments
```

Retrieves authorizations that don't have associated appointments.

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| startDate | query | Start date in YYYY-MM-DD format |
| endDate | query | End date in YYYY-MM-DD format |

## Report Endpoints

### List Clients

```
GET https://customerapi.alohaaba.com/v1/report/clients
```

Retrieves detailed information about the clients associated with a specific customer in Aloha.

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| clientId | integer | Unique identifier (PK) for the client |
| firstName | string | First name of the client (max length: 250) |
| lastName | string | Last name of the client (max length: 150) |
| aliasName | string | Alias or AKA of the client (max length: 150) |
| imageUrl | string/null | URL of the client's image if available (max length: 500) |
| officeId | integer | Unique identifier for the office |
| office | string | Office name (max length: 250) |
| isActive | boolean | Indicates whether the client is active |
| street | string | Street address (max length: 150) |
| city | string | City (max length: 50) |
| state | string | State (max length: 150) |
| zip | string | ZIP or postal code (max length: 50) |
| inActiveDate | string/null | Date when the client became inactive |

### List Appointments

```
GET https://customerapi.alohaaba.com/v1/report/appointments
```

Retrieves detailed information about appointments within a specified date range.

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| startDate | query | Start date in YYYY-MM-DD format |
| endDate | query | End date in YYYY-MM-DD format |

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| appointmentId | integer | Unique identifier for the appointment |
| clientId | integer | Unique identifier for the client |
| claimId | string/null | Identifier for the insurance claim (max length: 100) |
| appointmentDate | string | Date of appointment (mm-dd-yyyy format) |
| appointmentStart | string | Start time (hh:mm tt format) |
| appointmentEnd | string | End time (hh:mm tt format) |
| clientName | string | Name of the client (max length: 360) |
| staffName | string | Name of the staff member (max length: 360) |
| gender | string | Gender of the client (max length: 150) |
| appointmentLocation | string | Physical location (max length: 100) |
| patientAddress | string | Client's address (max length: 450) |
| insuredId | string | Client's insurance ID (max length: 100) |
| office | string | Office name (max length: 250) |
| renderingProviderNPI | string | Provider's NPI number (max length: 50) |
| renderingProvider | string | Name of service provider (max length: 360) |
| diagnosticCodes | string | Primary diagnostic code (max length: 150) |
| diagnosticCodes2 | string/null | Secondary diagnostic code (max length: 150) |
| diagnosticCodes3 | string/null | Tertiary diagnostic code (max length: 150) |
| payerName | string | Insurance payer name (max length: 250) |
| authorizationNumber | string | Authorization number (max length: 50) |
| chargeLineTimeZone | string/null | Time zone for charge line (max length: 500) |
| officeTimeZone | string | Office time zone (max length: 500) |
| serviceFacility | string | Service facility name (max length: 360) |
| serviceFacilityAddress | string | Facility address (max length: 450) |
| clientCity | string | Client's city (max length: 50) |
| billingAddress | string | Billing address (max length: 450) |
| canceledType | string | Type of cancellation (max length: 6) |
| serviceName | string | Name of service (max length: 150) |
| billingProviderNPI | string | Billing provider's NPI (max length: 50) |
| billingProvider | string | Name of billing provider (max length: 360) |
| billingCode | string | Billing code (max length: 210) |
| additionalCode | string/null | Additional billing code (max length: 100) |
| modifier | string/null | Primary modifier (max length: 150) |
| modifier2 | string/null | Secondary modifier (max length: 150) |
| modifier3 | string/null | Tertiary modifier (max length: 150) |
| placeOfService | integer/null | Place of service code |
| units | number | Number of units billed |
| unitSize | string | Unit size (e.g., minutes) (max length: 150) |
| charge | number | Amount charged |
| chargeRate | number | Rate per unit |
| contractRate | number | Contract rate per unit |
| contractAmount | number | Total contract amount |
| dob | string | Date of birth (mm-dd-yyyy format) |
| referringProviderName | string | Referring provider's name (max length: 360) |
| referringProviderNPI | string/null | Referring provider's NPI (max length: 50) |
| billingMinutes | number | Total billing minutes |
| billingHours | number | Total billing hours |
| completed | string | Completion status ("Yes"/"No") (max length: 3) |

### Client Authorization Details

The client authorization endpoints provide detailed information about service authorizations, usage, and availability. Below are the response fields for the client authorization endpoints:

#### Client Authorization Response Fields

| Field | Type | Description |
|-------|------|-------------|
| startDate | string | Start date of the authorization period |
| endDate | string | End date of the authorization period |
| scheduledAppointments | integer | Number of scheduled appointments |
| completedAppointments | integer | Number of completed appointments |
| scheduledHours | number | Total hours scheduled |
| completedHours | number | Total hours completed |
| rangeType | string | Type of date range used for the report |

#### Authorization Without Appointments Fields

| Field | Type | Description |
|-------|------|-------------|
| office | string | Office name and identifier |
| client_Name | string | Name of the client |
| payer_Name | string | Name of the insurance payer |
| iD_with_Payer | string | Client identifier with the payer |
| authorization_Number | string | Authorization reference number |
| referring_Provider | string | Name of referring provider |
| service_Name | string | Name and code of authorized service |
| allowed_Limit | integer | Maximum authorized units/visits |
| type | string | Type of limit (Units, Visits) |
| frequency | string | Authorization frequency |
| startDate | string | Authorization start date |
| endDate | string | Authorization end date |
| start_Date1 | string | Alternative start date if applicable |
| end_Date1 | string | Alternative end date if applicable |
| rendering_Provider | string | Name of provider delivering service |
| placeOfService | string | Location where service is provided |
| service_Facility | string | Facility where service is delivered |
| diagnostic_Codes | string | Primary diagnosis code |
| diagnostic_Codes2 | string | Secondary diagnosis code |
| diagnostic_Codes3 | string | Tertiary diagnosis code |
| client_Id | integer | Unique client identifier |
| payer_Id | integer | Unique payer identifier |
| authorizationGroupService_Id | integer | Unique service group identifier |

## Example Responses

### Example Generate AccessToken Response

```json
{
  "status": 200,
  "message": "Success",
  "data": {
    "username": "Aloha.Client.ACME",
    "accessToken": "eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9...",
    "accessTokenExpiration": "2024-06-01T01:41:19Z",
    "refreshToken": "ZNsAOKVqkN+XssUYuTAmPQBsJngCmipwggWm7Z9c4ug=",
    "subscriptionId": "2639f63e-e010-4a67-a267-c9be16e324e6"
  }
}
```

### Example List Client Response

```json
{
  "status": 200,
  "message": "Success",
  "data": [
    {
      "clientId": 101,
      "firstName": "Alice",
      "lastName": "Winston",
      "aliasName": "AW1234",
      "imageUrl": "https://example.com/images/alice.jpg",
      "officeId": 10,
      "isActive": true,
      "street": "1023 Willow Lane",
      "city": "Miami",
      "state": "Florida",
      "zip": "33101",
      "inActiveDate": null
    }
  ]
}
```

### Example List Appointments Response

```json
{
  "status": 200,
  "message": "Success",
  "data": [
    {
      "appointmentId": 12345,
      "clientId": 101,
      "appointmentDate": "03-15-2024",
      "appointmentStart": "09:00 AM",
      "appointmentEnd": "10:00 AM",
      "clientName": "Winston, Alice",
      "staffName": "Smith, John",
      "serviceName": "ABA Therapy",
      "billingCode": "97153",
      "units": 4,
      "unitSize": "15 minutes",
      "completed": "Yes"
    }
  ]
}
```

### Example Client Authorizations Response

```json
{
  "status": 200,
  "message": "Success",
  "data": [
    {
      "startDate": "2024-03-01",
      "endDate": "2024-03-31",
      "scheduledAppointments": 20,
      "completedAppointments": 18,
      "scheduledHours": 40.0,
      "completedHours": 36.0,
      "rangeType": "Monthly"
    }
  ]
}
```

### Example Billing Ledger Response

```json
{
  "status": 200,
  "message": "Success",
  "data": [
    {
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
    }
  ]
}
```

## Common Error Responses

### Authentication Error (401)
```json
{
  "status": 401,
  "message": "Authentication Failed",
  "errors": [
    {
      "name": "AuthenticationError",
      "message": "Invalid or expired access token"
    }
  ]
}
```

### Validation Error (400)
```json
{
  "status": 400,
  "message": "Validation Failed",
  "errors": [
    {
      "name": "ValidationError",
      "message": "startDate must be in YYYY-MM-DD format"
    }
  ]
}
```

### Not Found Error (404)
```json
{
  "status": 404,
  "message": "Not Found",
  "errors": [
    {
      "name": "NotFoundError",
      "message": "Client with ID 12345 not found"
    }
  ]
}
```

## Additional Notes

1. For technical support or questions about API access, reach out through the official support channels.
2. In case of `500` responses or other server errors, the service typically recovers within 15 minutes. If issues persist, contact support.
3. For information about API terms of use and privacy policy, refer to the official documentation.