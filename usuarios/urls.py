from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
]