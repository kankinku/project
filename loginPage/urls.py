
from django.urls import path
from loginPage import views


urlpatterns = [
    path("", views.auth_view,name="auth"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('create_class/', views.create_class, name='create_class'),
    path('delete_class/', views.delete_class, name='delete_class'),
]

