import google.oauth2.credentials
import google_auth_oauthlib.FLow

state = request.session['state']
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file.(
'client_secret.json',
scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
state=state)

authorization_response = request.GET.get('code')

flow.fetch_token(authorization_response=authorization_response)

credentials = flow.credentials
request.session['credentials'] ={
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'token_uri': credentials.token_uri,
    'client_id': credentials.client_id,
    'client_secret': credentials.client_secret,
    'scopes': credentials.scopes}
