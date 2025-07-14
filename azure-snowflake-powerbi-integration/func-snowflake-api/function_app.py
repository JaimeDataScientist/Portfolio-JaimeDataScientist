import logging
import azure.functions as func
import snowflake.connector
import os
import base64
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_private_key():
    # Une las partes
    b64_key = (
        os.environ.get("PRIVATE_KEY_PART1", "") +
        os.environ.get("PRIVATE_KEY_PART2", "") +
        os.environ.get("PRIVATE_KEY_PART3", "")
    )
    if not b64_key:
        raise ValueError("Private key is missing")

    pem_key = base64.b64decode(b64_key)
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    return serialization.load_pem_private_key(
        pem_key,
        password=None,
        backend=default_backend()
    )

def connect_snowflake():
    """Connect to Snowflake using key pair authentication"""
    private_key = get_private_key()
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        private_key=private_key_bytes,
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"]
    )

@app.function_name(name="GetSnowflakeData")
@app.route(route="getsnowflakedata", methods=["POST"])
def get_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Snowflake query endpoint hit.")

    try:
        body = req.get_json()
        query = body.get("query")

        if not query:
            return func.HttpResponse("Missing 'query' in request body", status_code=400)

        conn = connect_snowflake()

        with conn.cursor() as cur:
            cur.execute(query)
            columns = [col[0] for col in cur.description]
            rows = cur.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        return func.HttpResponse(json.dumps(results, default=str), mimetype="application/json")

    except Exception as e:
        logging.exception("Error querying Snowflake")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)
