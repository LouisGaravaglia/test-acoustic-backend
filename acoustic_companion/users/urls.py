from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='Users Index Page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='User Dashboard'),
    path('registerUser/', views.register_user_view, name='register-user'),
    path('authorizeSpotify/', views.authorize_spotify_view, name='athorize-spotify'),
    path('requestAccessTokens/', views.request_access_tokens, name='request-access-tokens'),
    path('requestRefreshToken/', views.request_refresh_token, name='request-refresh-token'),
    #TRYING TO SEND A CSRF TOKEN WHEN USER FIRST ENTERS OUR SITE
    # path('getCSRF/', views.send_csrf_view, name='send-csrf'),
]