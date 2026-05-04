import os, re, random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from groq import Groq
from elevenlabs.client import ElevenLabs

VOICE_OPTIONS = {
    "adam":   "pNInz6obpgDQGcFmaJgB",
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "josh":   "TxGEqnHWrfWFTfGW9XjX",
}
DEFAULT_VOICE = "adam"

SYSTEM_PROMPT = (
    "You are a ruthless stand-up comedian who roasts consumer products. "
    "Be savage, specific, and hilarious — never generic. "
    "Write EXACTLY 2 punchy sentences. No asterisks, no markdown. Output only the roast."
)
FALLBACKS = [
    "This product looks like it was designed by someone who lost a bet with themselves. Even the recycling bin swiped left.",
    "Whoever greenlit this confused 'innovative' with 'irrelevant'. It's the participation trophy of consumer goods.",
    "This thing is so underwhelming, it makes disappointment look exciting. Return it before it lowers your IQ by proximity.",
    "This product screams 2am brainstorm with zero sleep and even less shame. The warranty expired before the box was opened.",
]

def generate_roast_text(title: str) -> str:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Product: {title[:150]}"},
            ],
            temperature=1.0,
            max_tokens=150,
        )
        clean = re.sub(r'[*_`#"]', "", res.choices[0].message.content.strip())
        return clean if len(clean) > 20 else random.choice(FALLBACKS)
    except Exception as e:
        print(f"[roast_generator] Groq error: {e}")
        return random.choice(FALLBACKS)


def generate_roast_audio(text: str, idx: int, voice: str = DEFAULT_VOICE) -> str | None:
    os.makedirs("voice", exist_ok=True)
    audio_path  = f"voice/roast_{idx}.mp3"
    backup_path = f"voice/roast_{idx}.txt"

    with open(backup_path, "w") as f:   # text backup always written first
        f.write(text)

    try:
        client   = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        voice_id = VOICE_OPTIONS.get(voice, VOICE_OPTIONS[DEFAULT_VOICE])
        chunks   = client.text_to_speech.convert(
            voice_id=voice_id, text=text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        with open(audio_path, "wb") as f:
            for chunk in chunks:
                if chunk: f.write(chunk)
        return audio_path
    except Exception as e:
        print(f"[roast_generator] ElevenLabs error: {e}")
        return None