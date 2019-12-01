from googleapiclient.discovery import build

def Youtube(credentials1):
    finalList = []

    #call the api to retieve the list of liked videos
    youtube = build('youtube', 'v3', credentials=credentials1)
    resp = youtube.videos().list(part="snippet", myRating="like").execute()

    #traverser the response by calling the api again with page token
    while("nextPageToken" in resp):
        for i in resp["items"]:
        #check for category of music and entertainment
            if i["snippet"]["categoryId"]=='24' or i["snippet"]["categoryId"]=='10':
                finalList.append(i['id'])

        resp = youtube.videos().list(part="snippet",
                                    myRating="like",
                                    pageToken=resp["nextPageToken"]).execute()

    return finalList
