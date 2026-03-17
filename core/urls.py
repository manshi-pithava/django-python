from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('index/', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
]