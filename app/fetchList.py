import google.oauth2.credentials
import google_auth_oauthlib.flow

flow = google_auth_oauthlib.flow.FLow.from_client_secrets_file(
'client_secret.json',
['https://www.googleapis.com/auth/youtube.force-ssl'])

flow.redirect_uri = '/auth'

authrization_url, state = flow.authrization_url(access_type="offline",
include_granted_scopes="true")
