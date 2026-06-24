KEYCLOAK_SERVER = "http://localhost:8080"

REALM = "ai-knowledge-agent"

CLIENT_ID = "ai-angular"

ISSUER = f"{KEYCLOAK_SERVER}/realms/{REALM}"

JWKS_URL = (
    f"{KEYCLOAK_SERVER}/realms/{REALM}"
    "/protocol/openid-connect/certs"
)