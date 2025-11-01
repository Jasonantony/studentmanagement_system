from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff', views.staff, name='staff'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout, name='logout'),
]
