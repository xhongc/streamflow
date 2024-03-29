import datetime
from pathlib import Path
import sys
import os

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(1, os.path.join(os.getcwd(), 'lib'))

SECRET_KEY = 'django-insecure-u5_r=pekio0@zt!y(kgbufuosb9mddu8*qeejkzj@=7uyvb392'

DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = "dj-flow_csrftoken"
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082"
]

# Application definition

INSTALLED_APPS = [
    'xadmin',
    'crispy_forms',
    'reversion',
    "corsheaders",
    "pipeline",
    "pipeline.engine",
    "pipeline.component_framework",
    "pipeline.eri",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "custom_plugins",
    "rest_framework",
    "applications.flow",
    "applications.task"

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "component.drf.middleware.AppExceptionMiddleware"
]

ROOT_URLCONF = 'dj_flow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'static', 'dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj_flow.wsgi.application'
TIME_ZONE = "Asia/Shanghai"
CELERY_TIMEZONE = 'Asia/Shanghai'
LANGUAGE_CODE = "zh-hans"
if os.getenv("dockerrun", "no") == "yes":
    REDIS_HOST = "redis"
    MYSQL_HOST = "db"
else:
    REDIS_HOST = "127.0.0.1"
    MYSQL_HOST = "127.0.0.1"

BROKER_URL = f"redis://{REDIS_HOST}:6379/4"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bomboo",  # noqa
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": MYSQL_HOST,
        "PORT": "3306",
        # 单元测试 DB 配置，建议不改动
        "TEST": {"NAME": "test_db", "CHARSET": "utf8", "COLLATION": "utf8_general_ci"},
    },
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 定义django中redis的位置,指定用redis的dbs
        "LOCATION": f"redis://{REDIS_HOST}:6379/0",
        "OPTIONS": {
            # django使用redis的默认客户端来进行操作.
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
# STATIC_ROOT = 'static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # noqa

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
IS_USE_CELERY = True

if IS_USE_CELERY:
    INSTALLED_APPS += ("django_celery_beat", "django_celery_results")
    CELERY_ENABLE_UTC = False
    ENABLE_UTC = False
    DJANGO_CELERY_BEAT_TZ_AWARE = False

    CELERY_TASK_SERIALIZER = "pickle"
    CELERY_ACCEPT_CONTENT = ['pickle', ]
    CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "component.drf.generics.exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "component.drf.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "NON_FIELD_ERRORS_KEY": "params_error",
}
JWT_AUTH = {
    # 过期时间，生成的took七天之后不能使用
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 刷新时间 之后的token时间值
    # 'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 请求头携带的参数
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}
SCHEDULE_TASK_POINT = "applications.task.tasks.run_by_task_in_celery"

try:
    from local_settings import *  # noqa
except ImportError:
    pass
