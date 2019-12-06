from django.shortcuts import render, redirect
import callAPI
import os
import google.oauth2.credentials as Cred
import google_auth_oauthlib.flow
from django import forms
from user.models import Profile
import google.auth.transport.requests
import requests


class instaForm(forms.Form):
    instaid = forms.CharField(label='Instagram ID', max_length=100)
# Create your views here.
def CreateNew(request):
    if request.method == 'POST':
        form = instaForm(request.POST)
        if form.is_valid():
            request.session['instaid'] = form.cleaned_data['instaid']
            return redirect(getToken)
    else:
        form = instaForm()
    return render(request, 'create.html', {'form': form})

def getToken(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/userinfo.profile',],)

    flow.redirect_uri = 'http://localhost:8080/auth'

    authorization_url, state = flow.authorization_url(access_type="offline",
    include_granted_scopes="true")

    return redirect(authorization_url)

def exchangeToken(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/userinfo.profile',],)

    flow.redirect_uri = 'http://localhost:8080/auth'

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] ={
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    if(callAPI.userInfo(credentials, request.session["instaid"])):
        return redirect("/"+request.session["instaid"])

    return render(request, 'auth.html')

def main(request):
    a = request.path
    a = a[1:len(a)-1]
    token = Profile.objects.filter(instaName__exact=a)[0].token

    cred1 = open("client_secret.json", "r")
    c = eval(cred1.read())["web"]
    credentials = Cred.Credentials(token=None, refresh_token=token, token_uri=c["token_uri"], client_id=c["client_id"], client_secret=c["client_secret"])
    request1 = google.auth.transport.requests.Request()
    credentials.refresh(request1)

    l = callAPI.Youtube(credentials)
    print(l)
    return render(request, 'basic.html', {"l": l})
