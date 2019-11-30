from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
import google.oauth2.credentials
import google_auth_oauthlib.flow

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
'client_secret.json',
scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],)

flow.redirect_uri = 'http://localhost:8080/auth'

# Create your views here.
def getToken(request):
    authorization_url, state = flow.authorization_url(access_type="offline",
    include_granted_scopes="true")

    return redirect(authorization_url)

def exchangeToken(request):
    authorization_response = request.GET.get('code')
    print("hello")
    print(authorization_response)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] ={
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    return render(request, 'auth.html')
