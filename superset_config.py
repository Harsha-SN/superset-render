import os


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv(
    "SUPERSET_SECRET_KEY",
    "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
)

GUEST_TOKEN_JWT_SECRET = os.getenv(
    "GUEST_TOKEN_JWT_SECRET",
    "CHANGE_THIS_TO_ANOTHER_LONG_RANDOM_SECRET"
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
        "https://YOUR-STREAMLIT-APP.streamlit.app",
    ],
}


# ============================================================
# EMBEDDING / IFRAME
# ============================================================

HTTP_HEADERS = {
    "X-Frame-Options": "ALLOWALL",
}

# If your Streamlit app is the only embedding application,
# replace this with your actual Streamlit URL.
FRAME_ANCESTORS = [
    "https://YOUR-STREAMLIT-APP.streamlit.app",
]


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

# Allow Shillelagh generic JSON API functionality.
SHILLELAGH_ALLOW_GENERIC_JSON = True


# ============================================================
# SHILLELAGH API URL ALLOWLIST
# ============================================================

ALLOWED_USER_DEFINED_URLS = [
    r"https://analytics-api-82mg\.onrender\.com/.*"
]


# ============================================================
# SHILLELAGH ADAPTERS
# ============================================================

SHILLELAGH_ADAPTERS = {
    "genericjsonapi":
        "shillelagh.adapters.api.generic_json.GenericJsonAPI"
}


# ============================================================
# SHILLELAGH CACHE / TEMP DIRECTORY
# ============================================================

SHILLELAGH_CACHE_DIR = "/app/superset_home"

SQLITE_TMPDIR = "/app/superset_home/tmp"


# ============================================================
# CACHE
# ============================================================

CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}


# ============================================================
# EXAMPLES
# ============================================================

SUPERSET_LOAD_EXAMPLES = False
