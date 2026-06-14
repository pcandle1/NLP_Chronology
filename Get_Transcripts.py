import json
import requests
import time


class Transcript_API:
    def __init__(self, api_key, base_url):
        self.API_KEY = api_key
        self.BASE_URL = base_url

    #Using the Transcript API service to retrieve transcript files from YouTube
    #Captures and returns in a dictionary
    def retrieve_Transcript(self, video_ids):
        batch_transcripts = {}

        for index, video_id in enumerate(video_ids, start=1):
            try:
                print(f"[{index}/{len(video_ids)}] Requesting via API: {video_id}...")

                params = {
                    "video_url": video_id,
                    "format": "json"
                }
                headers = {
                    "Authorization": f"Bearer {self.API_KEY}"
                }

                response = requests.get(self.BASE_URL, params=params, headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    flat_text = ""
                    if "segments" in data and isinstance(data["segments"], list):
                        flat_text = " ".join([segment.get("text", "") for segment in data["segments"]])
                    elif "transcript" in data:
                        flat_text = str(data["transcript"])
                    elif "text" in data:
                        flat_text = str(data["text"])

                    flat_transcript = " ".join(flat_text.split())

                    if flat_transcript.strip():
                        batch_transcripts[video_id] = flat_transcript
                        print(f"  ✅ Successfully retrieved text. (Length: {len(flat_transcript)} chars)")
                    else:
                        print(f"  ⚠️ Warning: Response empty. Keys: {list(data.keys())}")
                        batch_transcripts[video_id] = "N/A"
                else:
                    print(f"  Server Error {response.status_code}: {response.text}")
                    batch_transcripts[video_id] = "N/A"

                time.sleep(0.5)

            except Exception as e:
                print(f"  Critical network request error on {video_id}: {str(e)}")
                print("Stopping script to protect current session state.")
                break

        print("\n--- API RUN TERMINATED ---")
        print(f"🎯 Execution finished. Captured {len(batch_transcripts)} transcripts.")

        return batch_transcripts


    #transforms the output into a flat line for processing
    def parse_and_merge_transcripts_to_json(self, input_text_file, output_json_file):
        """
        Reads a text file containing 'video_id ||| [{'text': ...}]', parses the
        snippets, and outputs a clean, standardized JSON file.
        """
        import ast
        import json

        print(f"Processing raw snippets from {input_text_file}...")

        with open(input_text_file, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()

        master_dict = {}

        for line_num, line in enumerate(lines, start=1):
            if " ||| " not in line:
                continue

            video_id, snippet_body = line.split(" ||| ", 1)
            video_id = video_id.strip()

            try:
                snippet_list = ast.literal_eval(snippet_body.strip())

                if isinstance(snippet_list, list):
                    text_pieces = [segment.get('text', '') for segment in snippet_list]

                    clean_single_line = " ".join(text_pieces)
                    clean_single_line = " ".join(clean_single_line.split())

                    if clean_single_line:
                        master_dict[video_id] = clean_single_line
                else:
                    print(f"Row {line_num} data wasn't a list structure. Skipping.")

            except Exception as e:
                print(f"Failed to parse snippet formatting on row {line_num}: {e}")

        with open(output_json_file, "w", encoding="utf-8") as json_file:
            json.dump(master_dict, json_file, indent=4, ensure_ascii=False)

        print(f"Success. Compiled {len(master_dict)} records into JSON file at: '{output_json_file}'")
        return master_dict
