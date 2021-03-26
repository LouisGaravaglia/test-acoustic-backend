from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.middleware.csrf import get_token
import json
from .models import User
import math
import random
import base64
import requests

def index(request):
    return HttpResponse('Welcome to the Users page!')

def dashboard(request):
    return render(request, 'users/dashboard.html')

#WILL NEED TO REMOVE CSRF_EXEMPT AND FIGURE OUT HOW TO PASS CSRF TOKEN WITH HEADERS IN POST REQUEST
@csrf_exempt
def register_user_view(request):

    json_data=json.loads(request.body)
    data = json_data["data"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    username = data["username"]
    password = data["password"]

    User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

    return HttpResponse({"success": True, "csrf": csrf(request)})

@csrf_exempt
def authorize_spotify_view(request):
    state = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    possible_len = len(possible)

    for i in range(16):
        state += possible[random.randint(0, possible_len - 1)]

    client_id = "myClientID"
    client_secret = "myClientSecret"
    stateKey = 'spotify_auth_state'
    scope = 'user-read-private user-read-email'
    url = 'https://accounts.spotify.com/authorize?'
    redirect_uri = 'https://acoustic-backend.herokuapp.com/callbackSpotify/'

    my_params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }

    resp = requests.get(url, params=my_params)
    print(resp.status_code)


    return HttpResponse({"authorize": "finished authorize"})

@csrf_exempt
def callback_spotify_view(request):
    print('********************************')
    print(request.GET)
    return HttpResponse({"callback": "hit callbaack"})

#TRYING TO SEND A CSRF TOKEN WHEN USER FIRST ENTERS OUR SITE
# def send_csrf_view(request):
#     csrf_token = get_token(request)
#     return HttpResponse({"success": True, "csrf": csrf_token})