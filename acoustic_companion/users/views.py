from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.middleware.csrf import get_token
import json as simplejson 
import json
from .models import User
import math
import random
import base64
import requests
from decouple import config
from urllib.parse import urlencode
from .utils import create_base_64_header
import os

def index(request):
    return HttpResponse('Welcome to the Users page!')

def dashboard(request):
    return render(request, 'users/dashboard.html')

#WILL NEED TO REMOVE CSRF_EXEMPT AND FIGURE OUT HOW TO PASS CSRF TOKEN WITH HEADERS IN POST REQ
@csrf_exempt
def register_user_view(request):

    json_data=json.loads(request.body)
    data = json_data["data"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    username = data["username"]
    password = data["password"]
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username, password=password, access_token=access_token, refresh_token=refresh_token)

    return HttpResponse({"success": True})

@csrf_exempt
def authorize_spotify_view(request):
    button_clicked = request.GET['button_clicked']
    CLIENT_ID = os.environ.get('CLIENT_ID', config('CLIENT_ID'))
    REDIRECT_URI = os.environ.get('REDIRECT_URI', config('REDIRECT_URI'))
    STATE_KEY = os.environ.get('STATE_KEY', config('STATE_KEY'))
    print('***button_clicked: ' + button_clicked)
    print('***client_id: ' + CLIENT_ID)
    print('***redirect_uri: ' + REDIRECT_URI)
    print('***state_key: ' + STATE_KEY + button_clicked)

    my_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': STATE_KEY + button_clicked
    }

    base_url = 'https://accounts.spotify.com/authorize'
    query_string =  urlencode(my_params)
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)

@csrf_exempt
def request_access_tokens(request):
    code = request.GET['code']
    REDIRECT_URI = os.environ.get('REDIRECT_URI', config('REDIRECT_URI'))
    CLIENT_ID = os.environ.get('CLIENT_ID', config('CLIENT_ID'))
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', config('CLIENT_SECRET'))

    data = {
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    print('***access_token: ' + access_token)
    print('***token_type: ' + token_type)
    print('***refresh_token: ' + refresh_token)
    print('***expires_in: ', expires_in)
    print('***error: ', error)

    token_obj = {
        'access_token': access_token,
        'token_type': token_type,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'error': error
    }

    json_token = simplejson.dumps(token_obj)

    return HttpResponse(json_token, content_type='application/json')

@csrf_exempt
def request_refresh_token(request):
    refresh_token = request.GET['refresh_token']
    CLIENT_ID = os.environ.get('CLIENT_ID', config('CLIENT_ID'))
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', config('CLIENT_SECRET'))
    base64_header = create_base_64_header(CLIENT_ID, CLIENT_SECRET)

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data=data,
        headers={f'Authorization: Basic {base64_header}'}
    ).json()

    refresh_token = response.get('refresh_token')
    print('***refresh_token: ' + refresh_token)

    json_token = simplejson.dumps({'refresh_token': refresh_token})

    return HttpResponse(json_token, content_type='application/json')

#TRYING TO SEND A CSRF TOKEN WHEN USER FIRST ENTERS OUR SITE
# def send_csrf_view(request):
#     csrf_token = get_token(request)
#     return HttpResponse({"success": True, "csrf": csrf_token})