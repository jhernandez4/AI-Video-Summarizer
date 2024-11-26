from fastapi import FastAPI, HTTPException
import httpx
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptAvailable, VideoUnavailable, InvalidVideoId
import re
import google.generativeai as genai
from dotenv import load_dotenv
from pyswip import Prolog
from typing import Dict, List

load_dotenv()

# Initialize Prolog and load rules
prolog = Prolog()
with open('video_rules.pl', 'r') as file:
    prolog_rules = file.read()
    prolog.assertz(prolog_rules)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Style mapping for different content types
STYLE_MAPPING = {
    'tutorial': 'How-to Guide',
    'educational': 'Study Guide',
    'entertainment': 'Review',
    'coding': 'Code Tutorial',
    'cooking': 'Recipe Guide',
    'general': 'General Summary'
}

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

# INPUT: A string representing a YouTube PC, mobile, Shorts Link or Video ID. 
# OUTPUT: A string containing the video summary generated by the Gemini API.
@app.get('/video-summarizer')
async def video_summarizer(youtube_link: str):
    try:
        video_id = extract_video_id(youtube_link)
        available_languages = await get_languages(video_id)
        video_transcript = await get_captions(video_id, available_languages)

        # Analyze content type using Prolog
        content_analysis = analyze_content_type(video_transcript)

        # Generate summary based on content type
        summary = await generate_summary(video_transcript, content_analysis)

        return {
            "content_type": content_analysis['content_type'],
            "summary_style": content_analysis['summary_style'],
            "summary": summary
        }

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



# INPUT: A string containing the text to be summarized. 
# OUTPUT: A string with the summary generated using the Gemini API.
@app.get('/generate-summary/')
async def generate_summary(video_transcript: str, content_analysis: Dict) -> str:
    prompt = f"""Generate a summary of this text in the style of a {content_analysis['summary_style']}.
    This content has been classified as: {content_analysis['content_type']}.
    Optimize the summary accordingly: {video_transcript}"""
    
    response = model.generate_content(prompt)
    return response.text

def analyze_content_type(transcript: str) -> Dict:
    """Analyze content type using Prolog rules"""
    transcript_lower = transcript.lower()
    
    # Query Prolog for content type
    content_types = list(prolog.query(f"content_type('{transcript_lower}', Type)"))
    
    if content_types:
        detected_type = content_types[0]['Type'].decode('utf-8')
        return {
            'content_type': detected_type,
            'summary_style': STYLE_MAPPING.get(detected_type, 'General Summary')
        }
    else:
        return {
            'content_type': 'general',
            'summary_style': 'General Summary'
        }

# INPUT: A string representing the Video ID and a list of language codes. 
# OUTPUT: A string containing the full transcript of the video.
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

# INPUT: A string representing the Video ID of a YouTube video.  
# OUTPUT: A list of language codes (e.g., ['en', 'es', 'fr']) available.
async def get_languages(video_id: str):
    response = YouTubeTranscriptApi.list_transcripts(video_id)

    language_list = []

    # Get a list of available language codes
    for transcript in response:
        language_list.append(transcript.language_code)

    return language_list

# INPUT: A YouTube link as a string (PC, mobile, Shorts, or Video ID).  
# OUTPUT: A string containing the extracted Video ID from the link.  
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