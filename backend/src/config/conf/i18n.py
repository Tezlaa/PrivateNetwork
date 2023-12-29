from config.conf.environ import env


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

USE_I18N = True

LANGUAGE_CODE = env('LANGUAGE_CODE', cast=str, default='en-us')