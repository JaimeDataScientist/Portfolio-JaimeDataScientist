# API Endpoints

## Function App: `guidion-data-puller-api`

### GET /api/guidion_data_puller

**Description:**  
This endpoint connects to the external Guideon API using OAuth2 client credentials. It allows fetching service tickets filtered by creation or modification dates. The function is implemented as an Azure Function with secure environment-managed credentials.

---

### Production Endpoint

`https://guidion-data-puller-<my-app>.azurewebsites.net/api/guidion_data_puller?code={function_key}`

Example call:

https://guidion-data-puller-xyz.azurewebsites.net/api/guidion_data_puller?code={function_key}&createdFrom=2025-06-25T00:00:00Z&createdTo=2025-07-01T00:00:00Z


>  **Note**: The `code` query parameter is required for authentication (`AuthLevel.FUNCTION`).

---

### Requirements

- Method: `POST`
- Required query parameters:
  - `createdFrom`: ISO 8601 datetime (e.g., `2025-06-25T00:00:00Z`)
  - `createdTo`: ISO 8601 datetime (must be within 7 days of `createdFrom`)
- Optional query parameters:
  - `lastModifiedFrom`, `lastModifiedTo`
  - `pageNo`, `pageSize`
  - `contractExternalId`

All query parameters are passed to the external Guideon API.

---

### Authentication

- The Azure Function uses **function-level access** (`AuthLevel.FUNCTION`)
- The backend calls Guideon's API using OAuth2 with client credentials
- The following environment variables are required:
  - `TOKEN_URL`
  - `CLIENT_ID`
  - `CLIENT_SECRET`
  - `SCOPE` *(optional)*
  - `DATA_URL` *(endpoint for ticket data)*

---

### Request Example

```http
GET /api/guidion_data_puller?createdFrom=2025-06-25T00:00:00Z&createdTo=2025-07-01T00:00:00Z&code={function_key}
Host: guidion-data-puller-xyz.azurewebsites.net
