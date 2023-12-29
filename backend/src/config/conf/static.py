from config.conf.boilerplate import BASE_DIR


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static/',
)