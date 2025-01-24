import json
import logging
import secrets
import string
from datetime import datetime
from pathlib import Path

import requests
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# File paths
AUTH_DB = Path("auth/database.json")
KEYS_FILE = Path("auth/keys.json")

# Initialize storage files
for path in [AUTH_DB, KEYS_FILE]:
    path.parent.mkdir(exist_ok=True)
    if not path.exists():
        path.write_text("{}")


# Helper functions
def generate_api_key():
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "llmkey_" + "".join(secrets.choice(alphabet) for _ in range(32))


def hash_key(key: str):
    return pwd_context.hash(key)


def verify_key(plain_key: str, hashed_key: str):
    return pwd_context.verify(plain_key, hashed_key)


class ClientRegistration(BaseModel):
    client_name: str


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/register")
async def register_client(request: Request):
    """Handle registration with detailed error logging"""
    try:
        # Log raw request body
        raw_body = await request.body()
        logger.info(f"Raw request body: {raw_body.decode()}")

        # Parse JSON with error handling
        try:
            data = await request.json()
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON format")

        if "client_name" not in data:
            logger.error("Missing client_name in request")
            raise HTTPException(status_code=400, detail="client_name is required")

        # Generate and store key
        raw_key = generate_api_key()
        hashed_key = hash_key(raw_key)

        # Load keys with validation
        try:
            keys = json.loads(KEYS_FILE.read_text())
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted keys file: {str(e)}")
            keys = {}

        keys[raw_key] = {
            "client_name": data["client_name"],
            "created_at": datetime.now().isoformat(),
            "hashed_key": hashed_key,
            "active": True,
        }

        # Write keys with atomic replacement
        temp_file = KEYS_FILE.with_suffix(".tmp")
        temp_file.write_text(json.dumps(keys, indent=2))
        temp_file.replace(KEYS_FILE)

        return {"api_key": raw_key, "warning": "Store this key securely"}

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# Authentication dependency
async def api_key_auth(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    keys = json.loads(KEYS_FILE.read_text())
    stored_data = keys.get(api_key)

    if not stored_data or not stored_data["active"]:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not verify_key(api_key, stored_data["hashed_key"]):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key


# Chat endpoint (modified)
@app.post("/chat")
async def chat_endpoint(request: Request, api_key: str = Depends(api_key_auth)):
    data = await request.json()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": data.get("message", ""),
            "stream": False,
        },
    )

    return response.json()
