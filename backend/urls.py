from django.contrib import admin
from django.urls import path, include
from storage.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('storage/', include('storage.urls')),  # Include storage app URLs
    path('', home, name='home'),
]
