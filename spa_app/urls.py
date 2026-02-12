from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('login/', auth_views.LoginView.as_view(template_name='spa_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('manage/', views.manage_services, name='manage_services'),
    path('manage/add/', views.add_service, name='add_service'),
    path('manage/edit/<int:pk>/', views.edit_service, name='edit_service'),
    path('manage/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('manage/contact/add/', views.add_contact, name='add_contact'),
    path('manage/contact/edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('manage/contact/delete/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('finalize_payment/', views.finalize_payment, name='finalize_payment'),
    path('manage/history/', views.booking_history, name='booking_history'),
    path('manage/history/clear/', views.clear_booking_history, name='clear_booking_history'),
    path('manage/history/edit/<int:pk>/', views.edit_booking, name='edit_booking'),
    path('manage/history/delete/<int:pk>/', views.delete_booking, name='delete_booking'),
]
