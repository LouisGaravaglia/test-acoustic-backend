from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='Users Index Page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='User Dashboard'),
    path('registerUser/', views.register_user_view, name='register-user'),
    path('authorizeSpotify/', views.authorize_spotify_view, name='athorize-spotify'),
    path('callbackSpotify/', views.callback_spotify_view, name='callback-spotify'),
    #TRYING TO SEND A CSRF TOKEN WHEN USER FIRST ENTERS OUR SITE
    # path('getCSRF/', views.send_csrf_view, name='send-csrf'),
]