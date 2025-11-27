from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
]
