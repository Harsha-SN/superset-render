import os

# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

GUEST_TOKEN_JWT_SECRET = os.getenv("GUEST_TOKEN_JWT_SECRET")

ENABLE_GUEST_TOKEN = True

GUEST_ROLE_NAME = "Gamma"

PUBLIC_ROLE_LIKE = "Gamma"

GUEST_TOKEN_JWT_AUDIENCE = "superset"


# =========================================================
# EMBEDDING
# =========================================================

FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "EMBEDDABLE_CHARTS": True,
    "DISABLE_EMBEDDED_SUPERSET_LOGOUT": True,
}


# =========================================================
# CORS
# =========================================================

ENABLE_CORS = True

CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": [
        "https://data-analytics-ui.streamlit.app"
    ],
}


# =========================================================
# SECURITY / PROXY
# =========================================================

TALISMAN_ENABLED = False

ENABLE_PROXY_FIX = True

PREFERRED_URL_SCHEME = "https"

WTF_CSRF_ENABLED = False

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"


# =========================================================
# SUPERSET METADATA DATABASE
# =========================================================

SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

PREVENT_UNSAFE_DB_CONNECTIONS = False
