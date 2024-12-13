# YouTube Video Summarizer  
## Project Structure
- **static/**: Contains the HTML, CSS, and JavaScript files for the front-end of the web app.
- **app.py**: The FastAPI backend, which includes helper functions and an endpoint for generating summaries from a YouTube link.
- **requirements.txt**: A file that lists the Python dependencies required for the project. Install dependencies with `pip install -r requirements.txt`.
- **system_instruction.txt**: Contains system instructions for the Gemini API to guide the summarization process.
- **video_rules.pl**: Prolog rules used to analyze video transcriptions and identify the key content type to help generate a more accurate summary.
## Project Setup
### 1. Clone the Repo
```bash
git clone https://github.com/jhernandez4/AI-Video-Summarizer.git
cd AI-Video-Summarizer
```

### 2. Set Up the Virtual Environment

Create and activate the virtual environment to isolate the project dependencies.

#### Using macOS/Linux:

```bash
python3 -m venv virtualEnv
source virtualEnv/bin/activate
```

#### Using Windows:

```bash
py -3 -m venv virtualEnv
virtualEnv\Scripts\activate
```

### 3. Install the Dependencies

```bash
pip install -r requirements.txt
```
### 4. Install SWI-Prolog

Download and install SWI-Prolog from [their official website](https://www.swi-prolog.org/download/stable).

### 5. Run the App

```bash
fastapi dev app.py
```
