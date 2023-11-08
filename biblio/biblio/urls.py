
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('station.urls')),
    #path('reg/', include('users.urls')),
    path('user/', include('users.urls')),
]
