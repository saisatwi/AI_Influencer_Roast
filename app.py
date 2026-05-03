import streamlit as st
import requests
import os
from dotenv import load_dotenv
from roast_generator import generate_roast_text, generate_roast_audio, get_supported_model
from video_generator import create_roast_video

# Load API keys
load_dotenv(dotenv_path=".env")
RAINFOREST_KEY = os.getenv("RAINFOREST_KEY")
voice_id = os.getenv("ELEVENLABS_VOICE_ID", "1xGjguWhviQbtIy2dkrh")

# Ensure folders exist
os.makedirs("images", exist_ok=True)
os.makedirs("voice", exist_ok=True)
os.makedirs("video", exist_ok=True)

st.set_page_config(page_title="AI Influencer Roast", layout="wide")
st.title("🔥 AI Influencer Roast 🔥")

# Sidebar controls
use_demo = st.sidebar.checkbox("Demo Mode (skip ElevenLabs)", value=False)
roast_style = st.sidebar.selectbox("Roast Style", ["Savage", "Playful", "Influencer"])
persona = st.sidebar.selectbox("Persona", ["Tech Reviewer", "Fashion Blogger", "Gamer Roast"])

def run_search(query: str):
    url = "https://api.rainforestapi.com/request"
    params = {
        "api_key": RAINFOREST_KEY,
        "amazon_domain": "amazon.com",
        "type": "search",
        "search_term": query
    }
    with st.spinner("🔍 Searching Amazon..."):
        rainforest_data = requests.get(url, params=params).json()
    results = rainforest_data.get("search_results", [])

    if not results:
        st.warning("No products found.")
        return

    for idx, product in enumerate(results[:3]):
        st.markdown(f"## Variation {idx+1}")
        st.image(product.get("image"), caption=product.get("title"))
        st.write(f"**{product.get('title')}**")
        st.write(f"[View on Amazon]({product.get('link')})")

        # Roast text
        with st.spinner("🎤 Generating roast text..."):
            prompt = f"Write a {roast_style.lower()} roast in the style of a {persona} about: {product.get('title')}"
            roast_text = generate_roast_text(prompt)
        st.subheader("AI Roast Text")
        st.write(roast_text)

        # Roast audio
        audio_file = None
        if not use_demo:
            with st.spinner("🎧 Generating roast audio..."):
                audio_file = generate_roast_audio(roast_text, idx)
                st.audio(audio_file, format="audio/mp3")
        else:
            st.info("Demo mode active: skipping ElevenLabs audio.")
            audio_file = f"voice/demo_roast_{idx}.mp3"
            import wave, numpy as np
            with wave.open(audio_file, "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(44100)
                silence = (np.zeros(44100)).astype("int16").tobytes()
                f.writeframes(silence)
            st.audio(audio_file, format="audio/mp3")

        # Roast video
        if product.get("image") and audio_file:
            img_path = f"images/product_{idx}.jpg"
            try:
                img_data = requests.get(product["image"]).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
                with st.spinner("🎬 Creating roast video..."):
                    video_file = create_roast_video(img_path, audio_file, roast_text, idx)
                st.subheader("AI Roast Video")
                st.video(video_file)

                # Download button
                with open(video_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Roast Video",
                        data=f,
                        file_name=f"roast_video_{idx}.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Video generation failed: {e}")

        st.markdown("---")

    st.info(f"Groq model: {get_supported_model()} | ElevenLabs voice ID: {voice_id}")

# Search bar
query = st.text_input("Search Amazon products...", key="query_input")

if st.session_state.query_input:
    run_search(st.session_state.query_input)

if st.button("Search"):
    run_search(query)
