import base64
import hashlib
import os
import secrets
from urllib.parse import urlencode

from dotenv import load_dotenv
from fastapi import Request
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

auth_supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def create_pkce_verifier():
    return secrets.token_urlsafe(64)


def create_pkce_challenge(verifier: str):
    digest = hashlib.sha256(
        verifier.encode()
    ).digest()

    return base64.urlsafe_b64encode(
        digest
    ).rstrip(b"=").decode()


def get_google_login_url(
    redirect_to: str,
    code_challenge: str
):
    params = urlencode({
        "provider": "google",
        "redirect_to": redirect_to,
        "code_challenge": code_challenge,
        "code_challenge_method": "s256",
    })

    return (
        f"{SUPABASE_URL}/auth/v1/authorize?"
        f"{params}"
    )


def exchange_code(
    code: str,
    code_verifier: str
):
    return auth_supabase.auth.exchange_code_for_session({
        "auth_code": code,
        "code_verifier": code_verifier,
    })


def get_authenticated_user(access_token: str):
    client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    response = client.auth.get_user(access_token)

    return response.user

def get_current_user(request: Request):

    access_token = request.cookies.get(
        "access_token"
    )

    if access_token is None:
        return None

    try:
        return get_authenticated_user(
            access_token
        )

    except Exception:
        return None