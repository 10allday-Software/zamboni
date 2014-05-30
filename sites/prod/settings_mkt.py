from lib.settings_base import *
from mkt.settings import *
from settings_base import *

from .. import splitstrip
import private_mkt

SERVER_EMAIL = 'zmarketplaceprod@addons.mozilla.org'
SECRET_KEY = private_mkt.SECRET_KEY

DOMAIN = getattr(private_mkt, 'DOMAIN', 'marketplace.firefox.com')
SITE_URL = getattr(private_mkt, 'SITE_URL', 'https://' + DOMAIN)
STATIC_URL = os.getenv('CUSTOM_CDN', 'https://marketplace.cdn.mozilla.net/')
LOCAL_MIRROR_URL = '%s_files' % STATIC_URL
MIRROR_URL = LOCAL_MIRROR_URL

CSP_STATIC_URL = STATIC_URL[:-1]
CSP_IMG_SRC = CSP_IMG_SRC + (CSP_STATIC_URL,)
CSP_SCRIPT_SRC = CSP_SCRIPT_SRC + (CSP_STATIC_URL,)
CSP_STYLE_SRC = CSP_STYLE_SRC + (CSP_STATIC_URL,)

ADDON_ICON_URL = STATIC_URL + 'img/uploads/addon_icons/%s/%s-%s.png?modified=%s'
PREVIEW_THUMBNAIL_URL = (STATIC_URL +
        'img/uploads/previews/thumbs/%s/%d.png?modified=%d')
PREVIEW_FULL_URL = (STATIC_URL +
        'img/uploads/previews/full/%s/%d.%s?modified=%d')
# paths for uploaded extensions
FILES_URL = STATIC_URL + "%s/%s/downloads/file/%d/%s?src=%s"

PREVIEW_FULL_PATH = PREVIEWS_PATH + '/full/%s/%d.%s'

SESSION_COOKIE_DOMAIN = ".%s" % DOMAIN

# paths for uploaded extensions
USERPICS_URL = STATIC_URL + 'img/uploads/userpics/%s/%s/%s.png?modified=%d'
COLLECTION_ICON_URL = STATIC_URL + 'img/uploads/collection_icons/%s/%s.png?m=%s'


MEDIA_URL = STATIC_URL + 'media/'
ADDON_ICONS_DEFAULT_URL = MEDIA_URL + 'img/hub'
ADDON_ICON_BASE_URL = MEDIA_URL + 'img/icons/'
PRODUCT_ICON_URL = STATIC_URL + 'product-icons'

CACHE_PREFIX = 'marketplace.%s' % CACHE_PREFIX
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_PREFIX

SYSLOG_TAG = "http_app_addons_marketplace"
SYSLOG_TAG2 = "http_app_addons_marketplace_timer"
SYSLOG_CSP = "http_app_addons_marketplace_csp"

# Redis
REDIS_BACKEND = getattr(private_mkt, 'REDIS_BACKENDS_CACHE', private.REDIS_BACKENDS_CACHE)
REDIS_BACKENDS_CACHE_SLAVE = getattr(private_mkt, 'REDIS_BACKENDS_CACHE_SLAVE', private.REDIS_BACKENDS_CACHE_SLAVE)
REDIS_BACKENDS_MASTER = getattr(private_mkt, 'REDIS_BACKENDS_MASTER', private.REDIS_BACKENDS_MASTER)
REDIS_BACKENDS_SLAVE = getattr(private_mkt, 'REDIS_BACKENDS_SLAVE', private.REDIS_BACKENDS_SLAVE)

REDIS_BACKENDS = {
    'cache': REDIS_BACKEND,
    'cache_slave': REDIS_BACKENDS_CACHE_SLAVE,
    'master': REDIS_BACKENDS_MASTER,
    'slave': REDIS_BACKENDS_SLAVE,
}

## Celery

BROKER_URL = private_mkt.BROKER_URL

CELERYD_PREFETCH_MULTIPLIER = 1

LOGGING['loggers'].update({
    'z.task': { 'level': logging.DEBUG },
    'z.hera': { 'level': logging.INFO },
    'z.redis': { 'level': logging.DEBUG },
    'z.receipt': {'level': logging.ERROR },
    'elasticutils': {'level': logging.INFO },
    'caching': {'level': logging.ERROR },
})

STATSD_PREFIX = 'marketplace'

GRAPHITE_PREFIX = STATSD_PREFIX

CEF_PRODUCT = STATSD_PREFIX


IMPALA_BROWSE = True
IMPALA_REVIEWS = True

WEBAPPS_RECEIPT_KEY = private_mkt.WEBAPPS_RECEIPT_KEY
WEBAPPS_RECEIPT_URL = private_mkt.WEBAPPS_RECEIPT_URL

APP_PREVIEW = True
MIDDLEWARE_CLASSES = tuple(m for m in MIDDLEWARE_CLASSES if m not in (csp,))

WEBAPPS_UNIQUE_BY_DOMAIN = True

SENTRY_DSN = private_mkt.SENTRY_DSN

SOLITUDE_HOSTS = ('https://payments.firefox.com',)
SOLITUDE_OAUTH = {'key': private_mkt.SOLITUDE_OAUTH_KEY,
                  'secret': private_mkt.SOLITUDE_OAUTH_SECRET}

# Bug 748403
SIGNING_SERVER = private_mkt.SIGNING_SERVER
SIGNING_SERVER_ACTIVE = True
SIGNING_VALID_ISSUERS = ['marketplace.cdn.mozilla.net']

# Bug 793876
SIGNED_APPS_SERVER_ACTIVE = True
SIGNED_APPS_SERVER = private_mkt.SIGNED_APPS_SERVER
SIGNED_APPS_REVIEWER_SERVER_ACTIVE = True
SIGNED_APPS_REVIEWER_SERVER = private_mkt.SIGNED_APPS_REVIEWER_SERVER

CARRIER_URLS = splitstrip(private_mkt.CARRIER_URLS)


# Pass through the DSN to the Raven client and force signal
# registration so that exceptions are passed through to sentry
#RAVEN_CONFIG = {'dsn': SENTRY_DSN, 'register_signals': True}

MONOLITH_PASSWORD = private_mkt.MONOLITH_PASSWORD

# Payment settings.
APP_PURCHASE_KEY = DOMAIN
APP_PURCHASE_AUD = DOMAIN
# This must match private.SECRET in webpay settings.
APP_PURCHASE_SECRET = private_mkt.APP_PURCHASE_SECRET

PRODUCT_ICON_PATH = NETAPP_STORAGE + '/product-icons'
DUMPED_APPS_PATH = NETAPP_STORAGE + '/dumped-apps'
DUMPED_USERS_PATH = NETAPP_STORAGE + '/dumped-users'

if NEWRELIC_ENABLE:
    NEWRELIC_INI = '/etc/newrelic.d/marketplace.firefox.com.ini'

ES_USE_PLUGINS = True

BANGO_BASE_PORTAL_URL = 'https://mozilla.bango.com/login/al.aspx?'

WHITELISTED_CLIENTS_EMAIL_API = private_mkt.WHITELISTED_CLIENTS_EMAIL_API

POSTFIX_AUTH_TOKEN = private_mkt.POSTFIX_AUTH_TOKEN

POSTFIX_DOMAIN = DOMAIN

# IARC content ratings.
IARC_COMPANY = 'Mozilla'
IARC_ENV = 'prod'
IARC_MOCK = False
IARC_PASSWORD = private_mkt.IARC_PASSWORD
IARC_PLATFORM = 'Firefox'
IARC_SERVICE_ENDPOINT = 'https://www.globalratings.com/IARCProdService/IARCServices.svc'
IARC_STOREFRONT_ID = 4
IARC_SUBMISSION_ENDPOINT = 'https://www.globalratings.com/IARCProdRating/Submission.aspx'
IARC_ALLOW_CERT_REUSE = False

BOKU_SIGNUP_URL = 'https://developer.mozilla.org/en-US/Marketplace/Publishing/Pricing/Providers/Boku'

PRE_GENERATE_APKS = True
PRE_GENERATE_APK_URL = 'https://controller.apk.firefox.com/application.apk'
