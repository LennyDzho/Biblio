from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('reg/', views.register, name='registrate'),
    path('auth/', views.register, name='auth')
]