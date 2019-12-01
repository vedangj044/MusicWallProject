from django.shortcuts import render, redirect
import callAPI
import google.oauth2.credentials
import google_auth_oauthlib.flow


# Create your views here.
def getToken(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],)

    flow.redirect_uri = 'https://localhost:8080/auth'

    authorization_url, state = flow.authorization_url(access_type="offline",
    include_granted_scopes="true")

    return redirect(authorization_url)

def exchangeToken(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],)

    flow.redirect_uri = 'https://localhost:8080/auth'

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

    print(callAPI.Youtube(credentials))

    return render(request, 'auth.html')

def main(request, nameID):

    return render(request, 'auth.html')
