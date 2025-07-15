# utils/llm_utils.py

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes and structures lecture content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def generate_summary(transcript):
    prompt = f"Summarize the following lecture transcript:\n\n{transcript}"
    return get_completion(prompt)

def generate_notes(transcript):
    prompt = f"Break down the following lecture into clear, topic-wise organized notes:\n\n{transcript}"
    return get_completion(prompt)

def generate_flashcards(transcript):
    prompt = f"Generate flashcards in Q&A format based on the following lecture transcript:\n\n{transcript}"
    return get_completion(prompt)
