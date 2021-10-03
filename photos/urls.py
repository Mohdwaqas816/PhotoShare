from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='viewPhoto'),
    path('add/', views.addPhoto, name='addPhoto'),


    # reset password class base view
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="photos/reset_password.html"), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="photos/password_reset_done.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="photos/password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="photos/password_reset_complete.html"), name='password_reset_complete'),

]
