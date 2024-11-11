from fastapi import FastAPI, HTTPException
import httpx
import os
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
import re

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get("/get-captions/")
async def get_captions(video_id: str):
    languages = ['en']
    response = YouTubeTranscriptApi.get_transcript(video_id, languages)
    
    caption_transcript = ""

    for segment in response:
        caption_text = ' ' + segment['text'].replace('\n', ' ') + ' '
        caption_transcript = caption_transcript + caption_text

        print(segment['text'])

    return caption_transcript 

def extract_video_id(input_str: str) -> str:
    # Check if the input is already a valid video ID
    if re.match(r'^[0-9A-Za-z_-]{11}$', input_str):
        return input_str

    # Regular expression to capture video ID from web or mobile URL formats
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, input_str)

    if match:
        return match.group(1)
    else:
        raise HTTPException(status_code=400, detail="Invalid input format for YouTube video ID")