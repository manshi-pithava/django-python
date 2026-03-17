from django.urls import path

from .import views

urlpatterns=[
path('logout/', views.user_logout, name='logout'),
path('login/', views.user_login, name='login'),
path('register/', views.user_register, name='register'),
path("profile/", views.profile, name="profile"),


]
