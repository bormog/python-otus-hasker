from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('questions.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'questions.views.handler_404'