import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class Create_Playlist:
    def __init__(self, secrets_file, scopes):
        self.secrets_file = secrets_file
        self.scopes = scopes


    # Authenticating
    def get_authenticated_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.secrets_file, self.scopes)
        credentials = flow.run_local_server(port=0)
        return build("youtube", "v3", credentials=credentials)


    #Create a blank playlist
    def create_playlist(self, youtube, title, description=""):
        print(f"🎬 Creating playlist: '{title}'...")
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        )
        response = request.execute()
        playlist_id = response["id"]
        print(f"✨ Playlist created successfully! ID: {playlist_id}")
        return playlist_id


    #add videos in order to the playlist from a list
    def add_videos_to_playlist(self, youtube, playlist_id, video_ids):
        print(f"\n🚀 Injecting {len(video_ids)} videos chronologically...")
        for index, video_id in enumerate(video_ids, start=1):
            try:
                print(f"[{index}/{len(video_ids)}] Adding video ID: {video_id}...")
                request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                )
                request.execute()
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to add video {video_id}. Error: {e}")
