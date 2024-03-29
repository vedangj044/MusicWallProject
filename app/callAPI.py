from googleapiclient.discovery import build
import requests
from user.models import Profile, favoriteMusician


def Youtube(credentials1):
    finalList = []

# call the api to retieve the list of liked videos
    youtube = build('youtube', 'v3', credentials=credentials1)
    resp = youtube.videos().list(part="snippet", myRating="like").execute()

# traverser the response by calling the api again with page token
    while("nextPageToken" in resp):
        for i in resp["items"]:
            # check for category of music and entertainment
            pepcor = i["snippet"]["categoryId"]
            if(pepcor == '24' or pepcor == '10'):
                finalList.append(i['id'])

        resp = youtube.videos().list(part="snippet",
                                     myRating="like",
                                     pageToken=resp["nextPageToken"]).execute()

    return finalList


def userInfo(credentials, insta):
    # url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    url1 = "https://www.googleapis.com/oauth2/v1/userinfo?access_token="
    url = url1+str(credentials.token)
    resp = requests.get(url)
    repos = eval(resp.text)
    newEntry = Profile(firstName=repos["given_name"], lastName=repos["family_name"], instaName=insta, googleID=repos["id"], token=credentials.token)
    try:
        newEntry.save()
        return True
    except Exception as e:
        raise
