from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, JsonResponse
from django.middleware.csrf import get_token
import json
from .models import User
import math
import random
import base64
from requests import Request, post
from decouple import config
import os

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
    print('/////////////////////////////////')
    state = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    possible_len = len(possible)

    for i in range(16):
        state += possible[random.randint(0, possible_len - 1)]

    CLIENT_ID = os.environ.get('CLIENT_ID')
    stateKey = 'spotify_auth_state'
    url = 'https://accounts.spotify.com/authorize'
    redirect_uri = 'https://acoustic-backend.herokuapp.com/callbackSpotify/'

    my_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': redirect_uri,
        'state': stateKey
    }

    # req = Request('GET', 'https://accounts.spotify.com/authorize', params={
    #     'response_type': 'code',
    #     'redirect_uri': redirect_uri,
    #     'client_id': CLIENT_ID
    # })
    # prepped_url = req.prepare()
    # res = {'url': prepped_url}
    # my_response = json.dumps(res)

    resp = requests.get(url, params=my_params)
    print(resp)

    # print(resp.status_code)
    # print(resp.url)


    return HttpResponse({"authorize": "finished authorize"})

@csrf_exempt
def callback_spotify_view(request):
    print('********************************')
    # code = request.GET.get('code')
    # error = request.GET.get('error')
    # CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    # print('code: ' + code)

    # response = post('https://accounts.spotify.com/api/token', data={
    #     'grant_type': 'authorization_code',
    #     'code': code,
    #     'redirect_uri': redirect_uri,
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET
    # }).json()

    # acccess_token = response.get('access_token')
    # token_type = response.get('token_type')
    # refresh_token = response.get('refresh_token')
    # expires_in = response.get('expires_in')
    # error = response.get('error')

    # print('access_token: ' + access_token)

    return HttpResponse({"callback": "hit callbaack"})

#TRYING TO SEND A CSRF TOKEN WHEN USER FIRST ENTERS OUR SITE
# def send_csrf_view(request):
#     csrf_token = get_token(request)
#     return HttpResponse({"success": True, "csrf": csrf_token})