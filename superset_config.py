import os


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv(
    "SUPERSET_SECRET_KEY"
)

GUEST_TOKEN_JWT_SECRET = os.getenv(
    "GUEST_TOKEN_JWT_SECRET"
)


# ============================================================
# GUEST TOKEN / EMBEDDING
# ============================================================

ENABLE_GUEST_TOKEN = True

GUEST_ROLE_NAME = "Gamma"

PUBLIC_ROLE_LIKE = "Gamma"

GUEST_TOKEN_JWT_AUDIENCE = "superset"


FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "EMBEDDABLE_CHARTS": True,
    "DISABLE_EMBEDDED_SUPERSET_LOGOUT": True,
}


# ============================================================
# CORS
# ============================================================

ENABLE_CORS = True

CORS_OPTIONS = {
    "supports_credentials": True,

    "origins": [
        # Replace this with your REAL Streamlit URL
        "https://YOUR-STREAMLIT-APP.streamlit.app"
    ],
}


# ============================================================
# PROXY / HTTPS
# ============================================================

TALISMAN_ENABLED = False

ENABLE_PROXY_FIX = True

PREFERRED_URL_SCHEME = "https"


# ============================================================
# CSRF
# ============================================================

WTF_CSRF_ENABLED = False


# ============================================================
# SESSION COOKIE
# ============================================================

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"


# ============================================================
# SUPERSET METADATA DATABASE
# ============================================================

SQLALCHEMY_DATABASE_URI = (
    "sqlite:////app/superset_home/superset.db"
    "?check_same_thread=false"
)


# ============================================================
# DATABASE CONNECTION SECURITY
# ============================================================

PREVENT_UNSAFE_DB_CONNECTIONS = False


# ============================================================
# SHILLELAGH
# ============================================================

# Allow Generic JSON APIs through Shillelagh
SHILLELAGH_ALLOW_GENERIC_JSON = True


# ============================================================
# ALLOWED API URLS
# ============================================================

# Allow your Render Flask Analytics API
ALLOWED_USER_DEFINED_URLS = [
    r"^https://analytics-api-82mg\.onrender\.com/.*$"
]
