
from django.urls import path
from loginPage import views


urlpatterns = [
    path("", views.auth_view,name="auth"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]

