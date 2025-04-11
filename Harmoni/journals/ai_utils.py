import requests
from dotenv import load_dotenv
import os

load_dotenv()

ANALYSIS_API_URL = os.getenv('ANALYSIS_API_URL')
SENTIMENT_API_URL = os.getenv('SENTIMENT_API_URL')
API_KEY = os.getenv('API_KEY')

headers = {
    'Authorization': f'Bearer {API_KEY}'
}


def sentiment_analysis(journal_text):
    response = requests.post(
        SENTIMENT_API_URL,
        headers = headers,
        json = { "inputs": journal_text }
    )

    if response.status_code == 200:
        result = response.json()[0][0]
        return result['label']
    else:
        print(f"error {response.status_code}: {response.text}")
        return "unavailable"


def generate_analysis(journal_text, sentiment, mbti_type):
    prompt = f"""
                I want you to give an in depth analysis/advice or emotional response to a person for a journal entry
                based on their MBTI personality type in order to help them strive for their mental wellness and make their 
                daily life easier to navigate. I want you to respond as though you're talking to that person. Below are the
                journal entry, mood/emotional state of the person their and their respective mbti personality type:

                MBTI PERSONALITY TYPE: {mbti_type}
                EMOTIONAL STATE: {sentiment}
                JOURNAL_ENTRY: {journal_text}
             """
    
    response = requests.post(
        ANALYSIS_API_URL,
        headers = headers,
        json = { "inputs": prompt }
    )

    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"error {response.status_code}: {response.text}"