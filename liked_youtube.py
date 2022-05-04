import json 
import os 

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

class getLikedVideos:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        """Log Into Youtube, Copied from Youtube Data API"""
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

        # Get credentials and create an API client

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        flow.redirect_uri = "https://www.example.com/oauth2callback"
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client
    
    def get_liked_videos(self):
        """Grab Our Liked Videos & Create A Dictionary Of Important Song Information"""
        request = self.youtube_client.videos().list(
            part = "snippet,contentDetails,statistics",
            myRating = "like",
            maxResults = 50
        )
        response = request.execute()
        #collect each video and get important info
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            view_count = item["statistics"]["viewCount"]
            liked_count = item["statistics"]["likeCount"]
            thumbnails   = item["snippet"]["thumbnails"]["default"]["url"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                    item["id"])

        #     use youtube_dl to collect the song name & artist name
            try:
                video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
                song_name = video["track"]
                artist = video["artist"]

                if song_name is not None and artist is not None:
                     self.all_song_info[video_title] = {
                        "song_name": song_name,
                        "artist": artist,
                        "youtube_url": youtube_url,
                        # "description" : description,
                        "view_count" : view_count,
                        "liked_count" :liked_count,
                        "thumbnails" :thumbnails,
                    }
            except:
                pass
            
            with open("liked_videos.json", "w") as files:
                json.dump(self.all_song_info, files)
 

if __name__ == '__main__':
    gLV = getLikedVideos()
    gLV.get_liked_videos()

        