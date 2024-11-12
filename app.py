from fastapi import FastAPI, HTTPException
import httpx
import os
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get('/generate-summary/')
async def generate_summary(video_id: str) -> str:
    video_transcript = await get_captions(video_id)
    category = ['How-to Guide', 'Study Guide', 'Recipe', 'Comparison', 'Tutorial', 'Study Notes', 'Review']

    response = model.generate_content(f'Generate a summary of this text in the style of a {category[-1]}: {video_transcript}')

    return response.text

@app.get("/get-captions/")
async def get_captions(video_id: str):
    languages = await get_languages(video_id)

    # Get first available transcript from a language
    response = YouTubeTranscriptApi.get_transcript(video_id, languages)
    
    caption_transcript = ""

    for segment in response:
        caption_text = ' ' + segment['text'].replace('\n', ' ') 
        caption_transcript = caption_transcript + caption_text

    return caption_transcript 

async def get_languages(video_id: str):
    response = YouTubeTranscriptApi.list_transcripts(video_id)
    
    language_list = []

    for transcript in response:
        language_list.append(transcript.language_code)

    return language_list

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