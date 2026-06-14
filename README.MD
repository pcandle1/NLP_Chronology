# NLP Chronology
I recently discovered the YouTube channel called ExtinctZoo where the creator details events and periods where different types of animals lived and went extinct. With 136 videos at the time of this project, there is plenty of content to keep me learning for a while. However, I prefer to digest the videos not in any particular order, but chronologically, from approximately 500 million years ago to the more recent topics. The content creator has not created a playlist with the videos in chronological order yet, although his website declares that he has plans to do so. This project is my attempt at ordering the videos using the transcripts from the videos, and some simple Natural Language Processing in order to automate a method to detect the likely time period for each video.

## Some Challenges
* As with most videos on YouTube, the videos have unhelpful titles, and thumbnails, meant to grab the users attention rather than give a good description of the information I am interested in.
* Youtube/Google does not give access to transcript files through their API, I ended up using a third party's API to access the transcripts I needed

## Tools
* Python with various Libraries, using Pycharm IDE
* YouTube Developer API
* TranscriptAPI (third party)

## How to run
In order to run my python code, download all files and run from the main file. I provided a prepared JSON file that skips the need to utilize the API's to retrieve the video ID's and the transcripts. 

## Key Objective and Results
I was able to successfully process the data and create an ordered playlist using elementary NLP. I created the playlist using YouTube's API, and the code will be saved for future projects that have overlap with this type of processing and work on YouTube.

## Repository Contents
├── prepared data/  
├── scripts/  
├── main/   
└── README.md
