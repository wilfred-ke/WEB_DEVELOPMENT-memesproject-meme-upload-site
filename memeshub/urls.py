from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.index, name="homepage"),
    path('signup', views.signup, name="signup"),
    path('signIn', views.signIn, name="signIn"),
    path('signOut', views.custom_logout, name="signOut"),
    path('check',views.check, name="check_email"),
    path('upload', views.upload, name="upload"),
    path('about', views.about, name="about"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('blogs', views.blogs, name="blogs"),
    path('privacy', views.privacy, name='privacy'),
    path('discover', views.discover, name='discover'),
    path('explore', views.explore, name='explore'),
    path('delete_post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('remove_profile_picture/', views.remove_profile_picture, name='remove_profile_picture'),
    path('like-image', views.like_image, name='like-image'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('file/<uuid:file_id>/', views.image_detail, name='image_detail'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('follow', views.follow, name="follow"),
    path('following', views.following, name='following'),
    path('offline', views.offline, name="offline"),
    path('user_settings', views.user_settings, name="user_settings"), 
    path('robots.txt', views.robots, name='robots.txt'),
    path('signIn', auth_views.LoginView.as_view(template_name="signIn.html"), name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name='password_reset_complete'),
              
]
handler404 = 'memeshub.views.handler404'
handler500 = 'memeshub.views.handler500'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


