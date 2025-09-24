from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt_validator import validate_jwt, create_auth_info

JWKS_URI = "https://your-tenant.logto.app/oidc/jwks"
ISSUER = "https://your-tenant.logto.app/oidc"

class AuthInfo:
    def __init__(
        self,
        sub: str,
        client_id: str = None,
        organization_id: str = None,
        scopes: list = None,
        audience: list = None,
    ):
        self.sub = sub
        self.client_id = client_id
        self.organization_id = organization_id
        self.scopes = scopes or []
        self.audience = audience or []

    def to_dict(self):
        return {
            "sub": self.sub,
            "client_id": self.client_id,
            "organization_id": self.organization_id,
            "scopes": self.scopes,
            "audience": self.audience,
        }


class AuthorizationError(Exception):
    def __init__(self, message: str, status: int = 403):
        self.message = message
        self.status = status
        super().__init__(self.message)


def extract_bearer_token_from_headers(headers: dict) -> str:
    """
    Extract bearer token from HTTP headers.

    Note: FastAPI and Django REST Framework have built-in token extraction,
    so this function is primarily for Flask and other frameworks.
    """
    authorization = headers.get("authorization") or headers.get("Authorization")

    if not authorization:
        raise AuthorizationError("Authorization header is missing", 401)

    if not authorization.startswith("Bearer "):
        raise AuthorizationError('Authorization header must start with "Bearer "', 401)

    return authorization[7:]  # Remove 'Bearer ' prefix


security = HTTPBearer()

async def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthInfo:
    try:
        token = credentials.credentials
        payload = validate_jwt(token)
        return create_auth_info(payload)

    except AuthorizationError as e:
        raise HTTPException(status_code=e.status, detail=str(e))