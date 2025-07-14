import azure.functions as func
import logging
import requests
import os

# Create a new Azure Function App with HTTP trigger, using FUNCTION-level authentication (requires API key)
#app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Define the route (URL path) that will trigger this function
#@app.route(route="guidion_data_puller")
#def guidion_data_puller(req: func.HttpRequest) -> func.HttpResponse:
def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("HTTP trigger received to pull Guidion tickets.")

    # -----------------------
    # 1. Get required query parameters from the request
    # These must be passed in the URL: createdFrom and createdTo
    # Example: ?createdFrom=2025-06-25T00:00:00Z&createdTo=2025-07-01T00:00:00Z
    # -----------------------
    created_from = req.params.get("createdFrom")
    created_to = req.params.get("createdTo")

    
    if not created_from or not created_to:
        return func.HttpResponse(
            "Missing required query parameters: createdFrom and createdTo.",
            status_code=400
        )

    # -----------------------
    # 2. Get optional parameters (can be passed in the URL or stored in environment)
    # -----------------------
    page_no = req.params.get("pageNo")     
    page_size = req.params.get("pageSize")        
    contract_id = req.params.get("contractExternalId")
    lastModifiedFrom = req.params.get("lastModifiedFrom")
    lastModifiedTo = req.params.get("lastModifiedTo")
    # -----------------------
    # 3. Read environment variables (from local.settings.json or Azure App Settings)
    # -----------------------
    token_url = os.environ.get("TOKEN_URL")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    scope = os.environ.get("SCOPE")                      # Optional, depending on API requirements
    data_url = os.environ.get("DATA_URL")

    # -----------------------
    # 4. Request OAuth token using client credentials (x-www-form-urlencoded)
    # -----------------------
    token_data = {
        #"grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
        #"scope": scope
    }
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        token_response = requests.post(token_url, data=token_data, headers=token_headers)
        logging.info(f"Token response status: {token_response.status_code}")
        logging.info(f"Token response body: {token_response.text}")
        token_response.raise_for_status()  # Raise error if status is not 200 OK
        access_token = token_response.json().get("access_token")
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return func.HttpResponse(f"Error obtaining token: {str(e)}", status_code=500)

    # -----------------------
    # 5. Prepare headers and query parameters to call the actual data API (/v2/tickets)
    # -----------------------
    query_params = {
        "createdFrom": created_from,
        "createdTo": created_to
    }

    if contract_id:
        query_params["contractExternalId"] = contract_id
    if lastModifiedFrom:
        query_params["lastModifiedFrom"] = lastModifiedFrom
    if lastModifiedTo:
        query_params["lastModifiedTo"] = lastModifiedTo

    data_headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
    }

    if page_no:
        data_headers["Page-No"] = page_no
    if page_size:
        data_headers["Page-Size"] = page_size

    # -----------------------
    # 6. Call the API to get the ticket data
    # -----------------------
    try:
        data_response = requests.get(data_url, headers=data_headers, params=query_params)
        logging.info(f"Request URL: {data_response.url}")
        logging.info(f"Response status: {data_response.status_code}")
        logging.info(f"Response body: {data_response.text}")
        data_response.raise_for_status()
        return func.HttpResponse(data_response.text, status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return func.HttpResponse(f"Error fetching data: {str(e)}", status_code=500)
