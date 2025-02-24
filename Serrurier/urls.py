from django.urls import path
from . import  views
from django.contrib.auth import views as auth_views

app_name = 'Serrurier'

urlpatterns=[
  path('',views.home,name='home'),
  path('change_language/<str:lang>/', views.change_language, name='change_language'),
  # path('mail', views.create_view, name='create_view'),
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('register/', views.register_view, name='register'),
  path('soumettre_avis/', views.soumettre_avis, name='soumettre_avis'),
  path('services/', views.service, name='services'),
  path('contact/', views.contact_view, name='contact'),
  path('admin_contact', views.admin_contact, name='admin_contact'),

  



]

