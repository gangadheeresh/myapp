from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),  # your app urls
]

if settings.DEBUG:  # only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

