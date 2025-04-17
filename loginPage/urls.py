
from django.urls import path
from loginPage import views


urlpatterns = [
    path("", views.auth_view,name="auth"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('create_class/', views.create_class, name='create_class'),
    path('delete_class/', views.delete_class, name='delete_class'),
    path('grade_summary/', views.grade_summary, name='grade_summary'),
    path('delete/submit/', views.delete_selected_classes, name='delete_classes'),
    path('delete-classes/', views.delete_selected_classes, name='delete_selected_classes'),
]

