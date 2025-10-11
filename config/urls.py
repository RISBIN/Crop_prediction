"""
URL Configuration for Crop Prediction project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Core app (landing page, about, contact)
    path('', include('apps.core.urls')),

    # Accounts app (registration, login, profile)
    path('accounts/', include('apps.accounts.urls')),

    # Predictions app (crop prediction, history)
    path('predictions/', include('apps.predictions.urls')),

    # Admin panel app (datasets, model training, analytics)
    path('admin-panel/', include('apps.admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
