from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('', include('questions.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'views.handler_404'
handler500 = 'views.handler_500'

