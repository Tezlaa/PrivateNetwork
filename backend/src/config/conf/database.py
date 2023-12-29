from config.conf.boilerplate import BASE_DIR
from config.conf.environ import env


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DOCKER_RUN = env('DOCKER_RUN', cast=bool, default=False)

if DOCKER_RUN:
    # PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env('POSTGRES_DB', cast=str),
            "USER": env('POSTGRES_USER', cast=str),
            "PASSWORD": env('POSTGRES_PASSWORD', cast=str),
            "HOST": env('POSTGRES_HOST', cast=str) if DOCKER_RUN else 'localhost',
            "PORT": env('POSTGRES_PORT', cast=int),
        }
    }
else:
    # SQlite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }