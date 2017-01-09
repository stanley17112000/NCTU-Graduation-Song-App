from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import hashlib

# Create your views here.

def index( request ):
    if request.session.get('code', False):
        return render_to_response('index.html', {'Info': 'Logout', 'login_logout':'logout()', 'LoginMessage': 'Hello, ' + request.session.get('code')})

    else:
        return render_to_response('index.html', {'Info': 'Login', 'login_logout':'login()', 'LoginMessage': 'Anonymous'})

def callback( request ):

    return HttpResponse()

def auth( request ):
    if 'code' not in request.GET:
        return HttpResponse('')
    code = request.GET['code']
    print code
    response = requests.post( 'https://id.nctu.edu.tw/o/token/', data={
        'grant_type': 'authorization_code',
        'client_id' : 's2DJWGhPyOknIMHwdJRrgSzwpNjZ7OaoNt56z5tW',
        'code' : code,
        'client_secret' : 'hz6MZbYQxaKjxJCKyWhzG9cOih25SZdDvs2YIbcFJBuas8jXRCc9MiyyOXK56Av734aThysyCVifIt2AUTXgshHWDrjU8APD5AnmakdBo7zVNerUY3yrfZcDXVFwpOUK',
        'redirect_uri' : 'https://nctu106song.herokuapp.com/auth'
    })
    print response.text
    responseJson = json.loads( response.text )
    header = {'Authorization': 'Bearer ' + responseJson['access_token']}
    response = requests.get('https://id.nctu.edu.tw/api/profile/', headers = header)
    responseJson = json.loads( response.text )

    request.session['code'] = responseJson['username']
    return redirect( '/index/' )
@csrf_exempt
def vote( request ):

    if 'code' in request.session:
        sha1 = hashlib.sha1( request.session['code'] + 'stanley' + request.POST['voteFor'] )

        return render_to_response( 'vote.html', {'id':request.session['code'], 'voteFor' :request.POST['voteFor'] , 'validateHash': sha1.hexdigest()} )
    else:
        return HttpResponse('Vote failed')

@csrf_exempt
def logout( request ):




    request.session['code'] = None

    return HttpResponse("")
