import os

# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

if not SECRET_KEY:
    SECRET_KEY = "change-this-in-render"

GUEST_TOKEN_JWT_SECRET = os.getenv("GUEST_TOKEN_JWT_SECRET")

if not GUEST_TOKEN_JWT_SECRET:
    GUEST_TOKEN_JWT_SECRET = "change-this-in-render"

# =========================================================
# GUEST TOKEN / EMBEDDING
# =========================================================

ENABLE_GUEST_TOKEN = True

GUEST_ROLE_NAME = "Gamma"

PUBLIC_ROLE_LIKE = "Gamma"

GUEST_TOKEN_JWT_AUDIENCE = "superset"

# =========================================================
# FEATURE FLAGS
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
# SECURITY HEADERS
# =========================================================

TALISMAN_ENABLED = False

ENABLE_PROXY_FIX = True

PREFERRED_URL_SCHEME = "https"

WTF_CSRF_ENABLED = False

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"

# =========================================================
# SUPSERSET METADATA DATABASE
# =========================================================

SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

# Needed for Shillelagh/API connections
PREVENT_UNSAFE_DB_CONNECTIONS = False

# =========================================================
# CONTENT SECURITY WARNING
# =========================================================

CONTENT_SECURITY_POLICY_WARNING = False
