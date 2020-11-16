import re
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('', include('questions.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
] + [
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve, kwargs=dict(document_root=settings.MEDIA_ROOT))
]

handler404 = 'questions.views.handler_404'