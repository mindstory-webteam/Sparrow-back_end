from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main.views import custom_404  # ← Import directly

handler404 = custom_404  # ← Pass function, not string

urlpatterns = [
    path('admin/logout/',
         auth_views.LogoutView.as_view(next_page='/admin/login/'),
         name='admin-logout'),

    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('ventures.urls')),

    # ✅ Preview 404 page during development (DEBUG = True)
    path('404/', custom_404, name='404-preview'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)