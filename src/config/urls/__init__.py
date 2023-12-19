from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve as mediaserve
from django.conf.urls.static import static

from config.urls.schema.urls import schema_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/', include('config.urls.api.v1')),
    
    path('', include('config.urls.views_urls.urls'))
]

urlpatterns += schema_urls

if not settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>',
             mediaserve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>',
             mediaserve, {'document_root': settings.STATIC_ROOT}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    