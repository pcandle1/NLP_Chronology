from Get_Data import *
from Language_Processor import Language_Processing
import json
import pandas as pd
from Create_Playlist import *
import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Get_Transcripts import *

#reading in API codes
with open('YT_API.txt','r',encoding='utf-8') as file:
    YT_API = file.read().strip()

with open('TRANSCRIPT_API.txt','r',encoding='utf-8') as file:
    TRANS_API = file.read().strip()


API = YT_API
EXTINCTZOO = "UU0ggS8bt4v7NiZpDfGqNpZQ"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = "client_secret.json"
TRANSCRIPT_API = TRANS_API
TRANSCRIPT_URL = "https://transcriptapi.com/api/v2/youtube/transcript"


### Run this block to extract the video ID's from Youtube and save into a txt
# if __name__ == "__main__":

    # gd = Get_Data()
    # all_ids = gd.get_all_video_ids(EXTINCTZOO)

    # with open('id_file.txt','w',encoding='utf-8') as file:
    #     for id in all_ids:
    #         # Write each item followed by a newline character
    #         file.write(f"{item}\n")


## Run this block to use ids to retrieve transcripts
# if __name__ == "__main__":

    # with open('id_file.txt','r',encoding='utf-8') as file:
    #     all_ids = file.readlines().to_list()
    #
    # gt = Transcript_API(api_key=TRANSCRIPT_API,base_url=TRANSCRIPT_URL)
    #
    # transcript_results = gt.retrieve_Transcript(all_ids)
    #
    # with open('all_transcripts.txt','w',encoding='utf-8') as file:
    #     file.write(transcript_results)

## Run this block to create more usable data, condensing the transcripts into a flat line in a json rather than snipptets
# if __name__ == "__main__":
#     parse_and_merge_transcripts_to_json(input_text_file='all_transcripts.txt', output_json_file='all_transcripts.json')


## Run this block to perform NLP and determine the date info for each video
# if __name__ == "__main__":
#     with open('all_transcripts.json','r',encoding='utf-8') as file:
#         transcripts = json.load(file)
#
#     master_dict = {}
#
#     for video_id, transcript_text in transcripts.items():
#         LP = Language_Processing(transcript_text)
#
#         years, epoch = LP.extract_features()
#         year, epoch, confidence = LP.calculate_anchor_point(years, epoch)
#
#         master_dict[video_id] = {"year": year, "epoch": epoch, "conf":confidence}
#
#     with open("results.json", "w", encoding='utf-8') as file:
#         json.dump(master_dict, file, indent=4, ensure_ascii=False)


## Run this block to order the videos and prepare for building the playlist on YouTube
# if __name__ == "__main__":
#     with open("results.json", "r", encoding='utf-8') as file:
#         master_dict = json.load(file)
#
#     df = pd.DataFrame.from_dict(master_dict, orient='index')
#
#     df.index.name = 'video_id'
#
#     df_sorted = df.sort_values("year", ascending=False)
#
#     ordered_playlist_ids = df_sorted.index.to_list()
#
#     with open('ordered_playlist.txt','w',encoding='utf-8') as file:
#             for id in ordered_playlist_ids:
#                 file.write(f"{item}\n")

## Run this block to create an empty playlist on YouTube, then populate with ordered videos
# if __name__ == "__main__":

#     cp = Create_Playlist(CLIENT_SECRETS_FILE, SCOPES)
#
#
#     youtube_service = cp.get_authenticated_service()
#
#     target_playlist_title = "ExtinctZoo Chronological Deep-Time Timeline"
#
#     new_playlist_id = cp.create_playlist(
#         youtube=youtube_service,
#         title=target_playlist_title,
#         description="A complete evolutionary timeline automatically ordered by NLP."
#     )
#
#     cp.add_videos_to_playlist(
#         youtube=youtube_service,
#         playlist_id=new_playlist_id,
#         video_ids=ordered_playlist_ids
#     )

