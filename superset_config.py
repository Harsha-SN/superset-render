# ============================================================
# SECRET KEY
# ============================================================

SECRET_KEY = "my-superset-secret-key-2026-change-this-to-a-long-random-value"


# ============================================================
# METADATA DATABASE
# ============================================================

SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"


# ============================================================
# DATABASE CONNECTION SECURITY
# ============================================================

PREVENT_UNSAFE_DB_CONNECTIONS = False


# ============================================================
# EMBEDDED SUPERSET
# ============================================================

FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "EMBEDDABLE_CHARTS": True,
    "DISABLE_EMBEDDED_SUPERSET_LOGOUT": True,
}

ENABLE_GUEST_TOKEN = True

GUEST_ROLE_NAME = "Gamma"

PUBLIC_ROLE_LIKE = "Gamma"

GUEST_TOKEN_JWT_AUDIENCE = "superset"


# ============================================================
# GUEST TOKEN SECRET
# ============================================================

GUEST_TOKEN_JWT_SECRET = "superset"


# ============================================================
# CORS
# ============================================================

ENABLE_CORS = True

CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": [
        "https://data-analytics-ui.streamlit.app",
    ],
}


# ============================================================
# SECURITY / PROXY
# ============================================================

TALISMAN_ENABLED = False

ENABLE_PROXY_FIX = True

PREFERRED_URL_SCHEME = "https"

WTF_CSRF_ENABLED = False


# ============================================================
# SESSION
# ============================================================

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"