"""
Django settings for sparrow_project project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%e=-vk=_d$++mgbmgyl9okepahzqa*%%s*lpkzkqdb6pao-nkh'

DEBUG = True  # Change to False when deploying

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'sparrowgroup.in', 'www.sparrowgroup.in']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'ventures',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.Custom404Middleware',  # ✅ Custom 404 (works with DEBUG=True & False)
]

ROOT_URLCONF = 'sparrow_project.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Required for 404.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ventures.context_processors.ventures_navigation',
            ],
        },
    },
]

WSGI_APPLICATION = 'sparrow_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Login / Logout redirect
LOGOUT_REDIRECT_URL = '/admin/login/'
LOGIN_REDIRECT_URL  = '/admin/'
LOGIN_URL           = '/admin/login/'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✅ EMAIL  (Career form → Hr@sparrowgroup.in)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# The site logs in to the Hr@sparrowgroup.in mailbox and sends the
# application email to HR. Fill in EMAIL_HOST_PASSWORD below.
#
# Pick the block that matches who hosts sparrowgroup.in email:
#   Google Workspace : smtp.gmail.com     587  TLS   (password = 16-letter App password)
#   Zoho Mail        : smtp.zoho.in       587  TLS   (mailbox password)
#   Microsoft 365    : smtp.office365.com 587  TLS   (mailbox password)
#   cPanel / hosting : mail.sparrowgroup.in 465 SSL  (mailbox password)
#                      → for 465 set EMAIL_USE_TLS = False and EMAIL_USE_SSL = True

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_USE_SSL       = False
EMAIL_HOST_USER     = 'Hr@sparrowgroup.in'
EMAIL_HOST_PASSWORD = 'PASTE-PASSWORD-HERE'      # ← put the App password / mailbox password here
EMAIL_TIMEOUT       = 20                         # seconds; the page never hangs on a slow mail server

DEFAULT_FROM_EMAIL  = f'Sparrow International Website <{EMAIL_HOST_USER}>'
SERVER_EMAIL        = EMAIL_HOST_USER

# Used by main/emails.py
COMPANY_NAME                   = 'Sparrow International'
CAREER_NOTIFY_EMAILS           = []      # extra copies (HR is always included automatically)
SEND_APPLICANT_ACKNOWLEDGEMENT = False   # True = also send a "we received your application" mail to the applicant
EMAIL_SEND_ASYNC               = True    # send in the background so the form submits instantly

# Show email errors in the runserver console (so you can see if a mail failed)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'main': {'handlers': ['console'], 'level': 'INFO'},
    },
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✅ SECURITY SETTINGS (for production)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER       = True
    SECURE_CONTENT_TYPE_NOSNIFF     = True
    X_FRAME_OPTIONS                 = 'DENY'
    SECURE_SSL_REDIRECT             = False  # Set True if using HTTPS
    SESSION_COOKIE_SECURE           = False  # Set True if using HTTPS
    CSRF_COOKIE_SECURE              = False  # Set True if using HTTPS

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# JAZZMIN SETTINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JAZZMIN_SETTINGS = {
    "site_title":        "Sparrow International",
    "site_header":       "Sparrow International",
    "site_brand":        "Sparrow Admin",
    "site_logo":         "images/admin-logo/logo4.png",
    "login_logo":        "images/admin-logo/logo3.png",
    "login_logo_dark":   "images/admin-logo/logo4.png",
    "site_logo_classes": "img-circle elevation-3",
    "site_icon":         "images/favicon/favicon.ico",
    "welcome_sign":      "Welcome to Sparrow International",
    "copyright":         "© 2026 Sparrow International",

    "search_model": ["auth.User"],

    "topmenu_links": [
        {"name": "Visit Website", "url": "/",           "new_window": True},
        {"name": "Dashboard",     "url": "admin:index"},
        {"model": "auth.User"},
    ],

    "usermenu_links": [
        {"name": "Visit Website", "url": "/", "new_window": True},
        {"name": "Logout", "url": "/admin/logout/", "new_window": False},
    ],

    "show_sidebar":           True,
    "navigation_expanded":    True,
    "order_with_respect_to": ["auth", "main", "ventures"],

    "icons": {
        "auth":                    "fas fa-shield-alt",
        "auth.user":               "fas fa-user-circle",
        "auth.group":              "fas fa-users",
        "main":                    "fas fa-layer-group",
        "main.brandlogos":         "fas fa-trademark",
        "main.careerapplications": "fas fa-file-alt",
        "main.jobroles":           "fas fa-briefcase",
        "main.journeymilestones":  "fas fa-road",
        "main.mapconnections":     "fas fa-project-diagram",
        "main.maplocations":       "fas fa-map-marker-alt",
        "main.teammembers":        "fas fa-user-tie",
        "ventures":                "fas fa-rocket",
        "ventures.sectors":        "fas fa-th-large",
        "ventures.ventures":       "fas fa-building",
        "ventures.venturedetails": "fas fa-info-circle",
        "ventures.products":       "fas fa-box-open",
        "ventures.brands":         "fas fa-tags",
        "ventures.galleries":      "fas fa-images",
        "main.herobanner":         "fas fa-photo-video",
        "main.programcategory":    "fas fa-folder-open",
        "main.programevent":       "fas fa-calendar-alt",
        "main.programimage":       "fas fa-photo-video",
    },

    "default_icon_parents":  "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-dot-circle",

    "related_modal_active":        True,
    "custom_css":                  "css/admin_custom.css",
    "custom_js":                   "js/admin_custom.js",
    "use_google_fonts_cdn":        True,
    "show_ui_builder":             False,
    "changeform_format":           "horizontal_tabs",
    "show_recent":                 True,
    "language_chooser":            False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":         False,
    "footer_small_text":         True,
    "body_small_text":           False,
    "brand_small_text":          False,
    "brand_colour":              "navbar-dark",
    "accent":                    "accent-danger",
    "navbar":                    "navbar-dark",
    "no_navbar_border":          True,
    "navbar_fixed":              True,
    "layout_boxed":              False,
    "footer_fixed":              False,
    "sidebar_fixed":             True,
    "sidebar":                   "sidebar-dark-primary",
    "sidebar_nav_small_text":    False,
    "sidebar_disable_expand":    False,
    "sidebar_nav_child_indent":  True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style":  False,
    "sidebar_nav_flat_style":    False,
    "theme":                     "flatly",
    "dark_mode_theme":           "darkly",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-outline-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
    "actions_sticky_top": True,
}