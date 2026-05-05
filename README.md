AI Influencer Roast

🎯 Overview
AI Influencer Roast is a creator‑ready pipeline that transforms Amazon product listings into short, vertical roast videos styled like influencer content. It combines product search, generative AI, voice synthesis, and video rendering into a seamless workflow — delivering clips that are instantly shareable on TikTok, Instagram, and YouTube Shorts.

This project demonstrates how technical innovation can be packaged into a business‑ready product: not just an app, but a content engine for creators, brands, and entertainment platforms.

# Demo video:
 Part-1 : https://www.loom.com/share/f82cc412ed86454c88e10b8ee1910752
 Part-2 : https://www.loom.com/share/8acb43107eab437b90be098853b0e612

🚀 Vision & Strategy
Creator Economy Alignment: Short‑form video dominates social platforms. AI Influencer Roast taps directly into this trend by automating roast content creation.

Differentiation: Unlike generic product review apps, this pipeline produces sarcastic influencer‑style commentary — a niche with viral potential.

Scalability: Built with modular APIs (Rainforest, Groq, ElevenLabs), the system can expand into other verticals (fashion, tech reviews, meme content).

Monetization Potential:

SaaS subscription for creators.

Branded roast campaigns for companies.

Viral marketing tool for e‑commerce.

🛠️ Technical Foundation
Data Layer: Amazon product search via SERP API.

AI Layer: Roast text generation using Groq LLMs.

Voice Layer: ElevenLabs TTS with demo mode fallback.

Video Layer: MoviePy/PIL pipeline for vertical video with captions overlay.

UX Layer: Streamlit app with progress indicators, persona/style selectors, and download/share buttons.

Resilience: Demo mode prevents crashes when quotas run out; organized folders (images/, voice/, video/) keep outputs clean.

📈 Business Impact
For creators: Instant roast clips ready for social media.

For companies: A showcase of how AI can generate viral content around products.

For investors: Proof of concept that blends technical robustness with market demand.

⚙️ Setup Instructions (Run on Any Computer)
Clone the repo

bash
git clone https://github.com/saisatwi/AI_Influencer_Roast.git
cd AI_Influencer_Roast
Create a virtual environment

bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Mac/Linux
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables

bash
streamlit run app.py
Generate roast videos

Search for a product.

Select persona & roast style.

Watch roast text, audio, and video generate in real time.
