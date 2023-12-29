from config.conf.environ import env


CORS_ALLOW_ALL_ORIGINS = True


ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=list, default=['*'])


# HTTPS Settings.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
