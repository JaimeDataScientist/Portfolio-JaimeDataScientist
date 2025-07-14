# Import standard libraries
import logging                          # For logging function events and errors
import azure.functions as func         # Azure Functions SDK
import snowflake.connector             # Snowflake Python connector
import os                              # To access environment variables
import base64                          # To decode the Base64-encoded private key
import json                            # To return results as JSON

# Import cryptography modules for private key handling
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Declare the Azure Function App using function-level authentication
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Function to retrieve and decode the private key from three environment variables
def get_private_key():
    # Concatenate the three Base64-encoded segments of the private key
    b64_key = (
        os.environ.get("PRIVATE_KEY_PART1", "") +
        os.environ.get("PRIVATE_KEY_PART2", "") +
        os.environ.get("PRIVATE_KEY_PART3", "")
    )

    # Raise an error if no key was found
    if not b64_key:
        raise ValueError("Private key is missing")

    # Decode the Base64 string into bytes (PEM format)
    pem_key = base64.b64decode(b64_key)

    # Deserialize the PEM key into a usable private key object
    return serialization.load_pem_private_key(
        pem_key,
        password=None,
        backend=default_backend()
    )

# Function to connect to Snowflake using key pair authentication
def connect_snowflake():
    """Establishes a secure connection to Snowflake using the decoded private key"""
    
    private_key = get_private_key()

    # Convert the private key object into the required DER binary format for Snowflake
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Return a Snowflake connection object using environment variables and the private key
    return snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        private_key=private_key_bytes,
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"]
    )

# Define the HTTP-triggered Azure Function endpoint
@app.function_name(name="GetSnowflakeData")
@app.route(route="getsnowflakedata", methods=["POST"])
def get_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Snowflake query endpoint hit.")

    try:
        # Parse JSON body of the request
        body = req.get_json()
        query = body.get("query")

        # Validate that a query string was included
        if not query:
            return func.HttpResponse("Missing 'query' in request body", status_code=400)

        # Establish connection to Snowflake
        conn = connect_snowflake()

        # Execute the SQL query and retrieve results
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [col[0] for col in cur.description]  # Get column names
            rows = cur.fetchall()                          # Get all result rows

        # Convert each row into a dictionary {column: value}
        results = [dict(zip(columns, row)) for row in rows]

        # Return the results as a JSON response
        return func.HttpResponse(json.dumps(results, default=str), mimetype="application/json")

    except Exception as e:
        # Log and return internal errors
        logging.exception("Error querying Snowflake")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)
