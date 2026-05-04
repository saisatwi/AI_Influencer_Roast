import streamlit as st
import requests
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch # Ensure pip install google-search-results
from roast_generator import generate_roast_text, generate_roast_audio
from video_generator import create_roast_video

load_dotenv()

# Workspace setup
for folder in ["images", "voice", "video"]:
    os.makedirs(folder, exist_ok=True)

st.set_page_config(page_title="AI Roast | SerpApi Edition", layout="wide")
st.title("🔥 AI Influencer Roast (Universal Search)")

# NEW API KEY HANDLING
SERP_KEY = os.getenv("SERPAPI_KEY")

query = st.text_input("Product Name (e.g., Casio Watch, Toy, Book):", placeholder="Enter item...")

if st.button("Generate Video", width='stretch'):
    if not query:
        st.error("Please enter a product.")
    else:
        status = st.empty()
        try:
            status.info(f"🔍 Searching Amazon for '{query}'...")
            
            # SERPAPI AMAZON ENGINE (2026 Logic)
            search = GoogleSearch({
                "engine": "amazon",
                "k": query,
                "api_key": SERP_KEY,
                "amazon_domain": "amazon.com",
                "type": "search"
            })
            data = search.get_dict()

            # The 'Catch-All' Extractor: Handles different Amazon layouts
            # We combine all possible result lists to ensure we find SOMETHING
            all_found = (
                data.get("organic_results", []) + 
                data.get("sponsored_products", []) + 
                data.get("shopping_results", [])
            )

            if not all_found:
                st.error("No results found. Try a more specific brand name.")
                st.stop()

            # Select the first item that has a valid image
            product = next((item for item in all_found if item.get("thumbnail")), all_found[0])
            title = product.get("title", "Unknown Product")
            img_url = product.get("thumbnail") or product.get("image")

            # 2. IMAGE DOWNLOAD (With standard headers to avoid 403)
            status.info("📸 Downloading media...")
            img_path = "images/raw_product.jpg"
            headers = {"User-Agent": "Mozilla/5.0"}
            img_data = requests.get(img_url, headers=headers).content
            
            with open(img_path, "wb") as f:
                f.write(img_data)

            # 3. ROAST & VOICE (Groq + ElevenLabs)
            status.info("🎙️ Generating Roast & Voice...")
            roast = generate_roast_text(title)
            st.markdown(f"**Script:** {roast}")
            
            audio_p = generate_roast_audio(roast, 0)
            
            # 4. FAST RENDER
            status.info("🎬 Rendering (Ultrafast Mode)...")
            video_p = create_roast_video(img_path, audio_p, roast, 0)
            
            if video_p:
                status.empty()
                st.video(video_p)
                st.success("Video generated successfully!")

        except Exception as e:
            st.error(f"Search failed: {str(e)}")