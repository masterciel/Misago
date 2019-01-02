# pylint: disable=line-too-long
"""
Django settings for dev project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Define placeholder gettext function
# This function will mark strings in settings visible to makemessages
# without need for Django's i18n features be initialized first.
_ = lambda s: s


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1znyfpwp*_#!r0#l248lht*6)_0b+504n*2-8cxf(2u)fhi0f^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# A list of strings representing the host/domain names that this Django site can serve.
# If you are unsure, just enter here your domain name, eg. ['mysite.com', 'www.mysite.com']

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        # Misago requires PostgreSQL to run
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": 5432,
    }
}


# Caching
# https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache

CACHES = {
    "default": {
        # Misago doesn't run well with LocMemCache in production environments
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ["username", "email"]},
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 7},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"


# User uploads (Avatars, Attachments, files uploaded in other Django apps, ect.)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

MEDIA_URL = "/media/"


# The absolute path to the directory where collectstatic will collect static files for deployment.
# https://docs.djangoproject.com/en/1.11/ref/settings/#static-root

STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Absolute filesystem path to the directory that will hold user-uploaded files.
# https://docs.djangoproject.com/en/1.11/ref/settings/#media-root

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder
# is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
# https://docs.djangoproject.com/en/1.10/ref/settings/#staticfiles-dirs

STATICFILES_DIRS = []


# Email configuration
# https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend

EMAIL_HOST = "localhost"
EMAIL_PORT = 25


# If either of these settings is empty, Django won't attempt authentication.

EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""


# Default email address to use for various automated correspondence from the site manager(s).

DEFAULT_FROM_EMAIL = "Forums <%s>" % EMAIL_HOST_USER


# Application definition

AUTH_USER_MODEL = "misago_users.User"

AUTHENTICATION_BACKENDS = ["misago.users.authbackends.MisagoBackend"]

CSRF_FAILURE_VIEW = "misago.core.errorpages.csrf_failure"

INSTALLED_APPS = [
    # Misago overrides for Django core feature
    "misago",
    "misago.users",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps used by Misago
    "celery",
    "debug_toolbar",
    "mptt",
    "rest_framework",
    "social_django",
    # Misago apps
    "misago.admin",
    "misago.acl",
    "misago.cache",
    "misago.core",
    "misago.conf",
    "misago.markup",
    "misago.legal",
    "misago.categories",
    "misago.threads",
    "misago.readtracker",
    "misago.search",
    "misago.faker",
]

INTERNAL_IPS = ["127.0.0.1"]

LOGIN_REDIRECT_URL = "misago:index"

LOGIN_URL = "misago:login"

LOGOUT_URL = "misago:logout"

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "misago.users.middleware.RealIPMiddleware",
    "misago.core.middleware.FrontendContextMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "misago.cache.middleware.cache_versions_middleware",
    "misago.conf.middleware.dynamic_settings_middleware",
    "misago.users.middleware.UserMiddleware",
    "misago.acl.middleware.user_acl_middleware",
    "misago.core.middleware.ExceptionHandlerMiddleware",
    "misago.users.middleware.OnlineTrackerMiddleware",
    "misago.admin.middleware.AdminAuthMiddleware",
    "misago.threads.middleware.UnreadThreadsCountMiddleware",
]

ROOT_URLCONF = "devproject.urls"

SOCIAL_AUTH_PIPELINE = (
    # Steps required by social pipeline to work - don't delete those!
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    # Uncomment next line to let your users to associate their old forum account with social one.
    # 'misago.users.social.pipeline.associate_by_email',
    # Those steps make sure banned users may not join your site or use banned name or email.
    "misago.users.social.pipeline.validate_ip_not_banned",
    "misago.users.social.pipeline.validate_user_not_banned",
    # Reads user data received from social site and tries to create valid and available username
    # Required if you want automatic account creation to work. Otherwhise optional.
    "misago.users.social.pipeline.get_username",
    # Uncomment next line to enable automatic account creation if data from social site is valid
    # and get_username found valid name for new user account:
    # 'misago.users.social.pipeline.create_user',
    # This step asks user to complete simple, pre filled registration form containing username,
    # email, legal note if you remove it without adding custom one, users will have no fallback
    # for joining your site using their social account.
    "misago.users.social.pipeline.create_user_with_form",
    # Steps finalizing social authentication flow - don't delete those!
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "misago.users.social.pipeline.require_activation",
)

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "misago.acl.context_processors.user_acl",
                "misago.conf.context_processors.conf",
                "misago.core.context_processors.site_address",
                "misago.core.context_processors.momentjs_locale",
                "misago.search.context_processors.search_providers",
                "misago.users.context_processors.user_links",
                # Data preloaders
                "misago.conf.context_processors.preload_settings_json",
                "misago.core.context_processors.current_link",
                "misago.markup.context_processors.preload_api_url",
                "misago.threads.context_processors.preload_threads_urls",
                "misago.users.context_processors.preload_user_json",
                # Note: keep frontend_context processor last for previous processors
                # to be able to expose data UI app via request.frontend_context
                "misago.core.context_processors.frontend_context",
            ]
        },
    }
]

WSGI_APPLICATION = "devproject.wsgi.application"


# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "misago.acl.panels.MisagoACLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
]


# Django Rest Framework
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "misago.core.rest_permissions.IsAuthenticatedOrReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "misago.core.exceptionhandler.handle_api_exception",
    "UNAUTHENTICATED_USER": "misago.users.models.AnonymousUser",
    "URL_FORMAT_OVERRIDE": None,
}


# Celery - Distributed Task Queue
# http://docs.celeryproject.org/en/latest/userguide/configuration.html

# Configure Celery to use Redis as message broker.

CELERY_BROKER_URL = "redis://redis:6379/0"

# Celery workers may leak the memory, eventually depriving the instance of resources.
# This setting forces celery to stop worker, clean after it and create new one
# after worker has processed 10 tasks.

CELERY_WORKER_MAX_TASKS_PER_CHILD = 10


# Misago specific settings
# https://misago.readthedocs.io/en/latest/developers/settings.html

# Complete HTTP address to your Misago site homepage. Misago relies on this address to create
# links in e-mails that are sent to site users.
# On Misago admin panel home page you will find a message telling you if you have entered the
# correct value, or what value is correct in case you've didn't.

MISAGO_ADDRESS = "http://my-misago-site.com/"


# On dev instance, generate only three sizes of avatars instead of default 6 sizes.

MISAGO_AVATARS_SIZES = [400, 200, 100]


# PostgreSQL text search configuration to use in searches
# Defaults to "simple", for list of installed configurations run "\dF" in "psql".
# Standard configs as of PostgreSQL 9.5 are: dutch, english, finnish, french,
# german, hungarian, italian, norwegian, portuguese, romanian, russian, simple,
# spanish, swedish and turkish
# Example on adding custom language can be found here: https://github.com/lemonskyjwt/plpstgrssearch

MISAGO_SEARCH_CONFIG = "simple"


# Allow users to download their personal data
# Enables users to learn what data about them is being held by the site without having
# to contact site's administrators.

MISAGO_ENABLE_DOWNLOAD_OWN_DATA = True

# Path to the directory that Misago should use to prepare user data downloads.
# Should not be accessible from internet.

MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR = os.path.join(BASE_DIR, "userdata")


# Allow users to delete their accounts
# Lets users delete their own account on the site without having to contact site administrators.
# This mechanism doesn't delete user posts, polls or attachments, but attempts to anonymize any
# data about user left behind after user is deleted.

MISAGO_ENABLE_DELETE_OWN_ACCOUNT = True


# Automatically delete new user accounts that weren't activated in specified time
# If you rely on admin review of new registrations, make this period long, disable
# the "deleteinactiveusers" management command, or change this value to zero. Otherwise
# keep it short to give users a chance to retry on their own after few days pass.

MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS = 2


# Path to directory containing avatar galleries
# Those galleries can be loaded by running loadavatargallery command

MISAGO_AVATAR_GALLERY = os.path.join(BASE_DIR, "avatargallery")


# Specifies the number of days that IP addresses are stored in the database before removing.
# Change this setting to None to never remove old IP addresses.

MISAGO_IP_STORE_TIME = 50


# Profile fields

MISAGO_PROFILE_FIELDS = [
    {
        "name": _("Personal"),
        "fields": [
            "misago.users.profilefields.default.RealNameField",
            "misago.users.profilefields.default.GenderField",
            "misago.users.profilefields.default.BioField",
            "misago.users.profilefields.default.LocationField",
        ],
    },
    {
        "name": _("Contact"),
        "fields": [
            "misago.users.profilefields.default.TwitterHandleField",
            "misago.users.profilefields.default.SkypeIdField",
            "misago.users.profilefields.default.WebsiteField",
        ],
    },
    {
        "name": _("IP address"),
        "fields": ["misago.users.profilefields.default.JoinIpField"],
    },
]


# Set dev instance to send e-mails to console

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Display debug toolbar if IN_MISAGO_DOCKER enviroment var is set to "1"

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "misago.conf.debugtoolbar.enable_debug_toolbar"
}
