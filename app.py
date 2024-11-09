from fastapi import FastAPI, HTTPException
import httpx
import os
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get("/get-captions/")
async def get_captions(video_id: str):
    response = YouTubeTranscriptApi.get_transcript(video_id)
    
    caption_transcript = ""

    for segment in response:
        caption_text = ' ' + segment['text'].replace('\n', ' ') + ' '
        caption_transcript = caption_transcript + caption_text

        print(segment['text'])

    return caption_transcript 