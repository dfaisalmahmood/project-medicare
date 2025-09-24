import os
import jwt
from jwt import PyJWKClient
from typing import Dict, Any
from auth_middleware import AuthInfo, AuthorizationError, JWKS_URI, ISSUER

jwks_client = PyJWKClient(JWKS_URI)


def validate_jwt(token: str) -> Dict[str, Any]:
    """Validate JWT and return payload"""
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={"verify_aud": False},  # We'll verify audience manually
        )

        verify_payload(payload)
        return payload

    except jwt.InvalidTokenError as e:
        raise AuthorizationError(f"Invalid token: {str(e)}", 401)
    except Exception as e:
        raise AuthorizationError(f"Token validation failed: {str(e)}", 401)


def create_auth_info(payload: Dict[str, Any]) -> AuthInfo:
    """Create AuthInfo from JWT payload"""
    scopes = payload.get("scope", "").split(" ") if payload.get("scope") else []
    audience = payload.get("aud", [])
    if isinstance(audience, str):
        audience = [audience]

    return AuthInfo(
        sub=payload.get("sub"),
        client_id=payload.get("client_id"),
        organization_id=payload.get("organization_id"),
        scopes=scopes,
        audience=audience,
    )


def verify_payload(payload: Dict[str, Any]) -> None:
    """Verify payload for global API resources"""
    # Check audience claim matches your API resource indicator
    audiences = payload.get('aud', [])
    if isinstance(audiences, str):
        audiences = [audiences]

    if os.getenv("API_RESOURCE_URL") not in audiences:
        raise AuthorizationError('Invalid audience')

    # Check required scopes for global API resources
    required_scopes = ['api:read', 'api:write']  # Replace with your actual required scopes
    scopes = payload.get('scope', '').split(' ') if payload.get('scope') else []
    if not all(scope in scopes for scope in required_scopes):
        raise AuthorizationError('Insufficient scope')