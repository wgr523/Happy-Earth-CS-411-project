from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('simpleIndex/', include('simpleIndex.urls')),
    path('admin/', admin.site.urls),
]
