import os
import requests
import wave
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from elevenlabs import ElevenLabs

# Load environment variables
load_dotenv(dotenv_path=".env")

groq_key = os.getenv("GROQ_API_KEY")
eleven_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("ELEVENLABS_VOICE_ID", "1xGjguWhviQbtIy2dkrh")

# Ensure folders exist
os.makedirs("voice", exist_ok=True)

groq_client = Groq(api_key=groq_key)
eleven_client = ElevenLabs(api_key=eleven_key)

def get_supported_model() -> str:
    """Fetch available Groq models and return a usable one."""
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {groq_key}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    for m in data.get("data", []):
        model_id = m.get("id", "")
        if "instruct" in model_id or "it" in model_id:
            return model_id
    if data.get("data"):
        return data["data"][0]["id"]
    raise RuntimeError("No supported Groq models found")

def generate_roast_text(product_title: str) -> str:
    """Generate roast text using Groq LLM with a live model."""
    model_id = get_supported_model()
    prompt = f"Write a sarcastic influencer-style roast about the product: {product_title}"
    response = groq_client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def generate_roast_audio(roast_text: str, idx: int = 0) -> str:
    """Convert roast text to audio using ElevenLabs, with quota fallback."""
    file_path = f"voice/roast_clip_{idx}.mp3"
    try:
        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=voice_id,
            text=roast_text
        )
        with open(file_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        return file_path
    except Exception as e:
        # Fallback: generate silent audio if quota exceeded
        with wave.open(file_path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(44100)
            silence = (np.zeros(44100)).astype("int16").tobytes()
            f.writeframes(silence)
        print(f"[Fallback] Audio generation failed: {e}")
        return file_path
