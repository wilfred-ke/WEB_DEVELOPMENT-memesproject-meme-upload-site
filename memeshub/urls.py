from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('signup', views.signup, name="signup"),
    path('signIn', views.signIn, name="signIn"),
    path('signOut', views.signOut, name="signOut"),
    path('check',views.check, name="check_email"),
    path('upload', views.upload, name="upload"),
    path('about', views.about, name="about"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('blogs', views.blogs, name="blogs"),
    path('privacy', views.privacy, name='privacy'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name='password_reset_complete'),
              
]
