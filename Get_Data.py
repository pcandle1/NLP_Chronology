from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

class Get_Data:
    def __init__(self,api):
        self.api = api
        self.youtube = build("youtube","v3",developerKey=api)


    def get_all_video_ids(self,channel_id) -> list:

        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(
                part="contentDetails",
                playlistId=self.youtube_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                vid_id = item["contentDetails"]["videoId"]
                video_ids.append(vid_id)

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

        return video_ids


    def simplify_data(self, transcript_file):
        simplified_transcripts = {}
        for video_id, transcript_data in transcript_file.items():
        # Extract just the 'text' key from every timestamp dictionary and join them with a space
            full_script = " ".join([entry['text'] for entry in transcript_data])

        # Clean up any weird spacing caused by joining line breaks
            full_script = " ".join(full_script.split())

        # Save it to our new dictionary
            simplified_transcripts[video_id] = full_script
        return simplified_transcripts