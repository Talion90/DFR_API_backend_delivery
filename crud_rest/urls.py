from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from crud_rest.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('delivery.api.profiles.urls')),
    path('', include('delivery.authentication.urls', namespace='authentication')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
