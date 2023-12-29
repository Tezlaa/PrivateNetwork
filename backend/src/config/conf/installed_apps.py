INSTALLED_APPS = [
    # packages
    'daphne',
    
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # packages
    'drf_yasg',
    'channels',
    'rest_framework',
    'rest_framework_simplejwt',
    # 'corsheaders',
    
    # apps
    'apps.chat',
    'apps.lobby',
    'apps.accounts',
    'apps.a12n',
    'apps.contact',
]