from fastapi import FastAPI, HTTPException
import httpx
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptAvailable, VideoUnavailable, InvalidVideoId
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

@app.get('/video-summarizer')
async def video_summarizer(youtube_link: str):
    try:
        video_id = extract_video_id(youtube_link)
        available_languages = await get_languages(video_id)
        video_transcript = await get_captions(video_id, available_languages)

    except InvalidVideoId:
        # Raised if video ID is invalid
        raise HTTPException(status_code=400, detail='Invalid video ID')

    except VideoUnavailable:
        # Raised if the video cannot be found or is unavailable
        raise HTTPException(status_code=404, detail="Video not found or unavailable")

    except NoTranscriptAvailable:
        # Raised if transcripts are unavailable for the video
        raise HTTPException(status_code=404, detail="Transcripts are unavailable for this video")

    except Exception as e:
        # Catch any other unforeseen errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    summary = await generate_summary(video_transcript)

    return summary

@app.get('/generate-summary/')
async def generate_summary(video_transcript: str) -> str:
    video_transcript = video_transcript
    category = ['How-to Guide', 'Study Guide', 'Recipe', 'Comparison', 'Tutorial', 'Study Notes', 'Review']

    response = model.generate_content(f'Generate a summary of this text in the style of a {category[-1]}: {video_transcript}')

    return response.text

@app.get("/get-captions/")
async def get_captions(video_id: str, languages: list[str]):
    languages = languages

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

    # Get a list of available language codes
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