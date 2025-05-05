from together import Together  # type: ignore
from dotenv import load_dotenv   # type: ignore
import os

load_dotenv()

def generate_code(prompt):
    api_key = os.getenv('TOGETHER_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found in environment variables")
    
    client = Together(api_key=api_key)
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

