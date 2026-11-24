from google import genai
from google.genai.errors import APIError
from sleep import sleep

ALL_FREE_GEMINI_MODELS = [
    # --- Core Text, Reasoning & Grounding (Best for your directory lookups) ---
    "gemini-4-hydrogen",          # Best overall free model; fast, multimodal, supports Google Search grounding
    "gemini-3.8-flash",           # Strongest free multi-step reasoning/parsing model (tighter daily rate limits)
    "gemini-3.6-flash",           # Previous-gen Flash; balanced speed and multimodality
    "gemini-3.5-flash-lite",      # High rate limits; ideal for bulk text parsing and formatting
    "gemini-3.1-flash-lite",      # Ultra-lightweight, low-latency fallback for simple extraction/tagging
    "gemini-3-flash-preview",     # Preview build for testing prompts (Google recommends 3.6/3.8 Flash over this)
    "gemini-2.5-flash-lite",      # Legacy Lite model (only works on projects that used it prior to deprecation)

    # --- Open-Weight Gemma Models (Hosted free on AI Studio; generous rate limits, no Search grounding) ---
    "gemma-4-31b-it",             # Strongest open Gemma model (31B dense); great for offline/local text parsing
    "gemma-4-26b-a4b-it",         # Mixture-of-Experts (26B total, ~4B active); fast with near-31B quality
    "gemma-4-e4b-it",             # Lightweight edge-sized Gemma 4 variant
    "gemma-4-e2b-it",             # Smallest ultra-fast Gemma 4 variant

    # --- Specialized Audio, Voice & Embedding Models (Not for text scraping, but free on the API) ---
    "gemini-3.8-live",            # Real-time low-latency bidirectional voice/video API
    "gemini-3.8-flash-tts",       # Text-to-speech audio generation
    "gemini-3.8-flash-lite-tts",  # Lightweight, fast text-to-speech
    "gemini-3.5-transcribe",      # Speech-to-text transcription with speaker diarization
    "gemini-embedding-2",         # Multimodal embeddings (for semantic search / matching school names)
    "gemini-embedding-001",       # Text embeddings
]
MODELS = ALL_FREE_GEMINI_MODELS
client = genai.Client()
max_tries = 3

def gemini(prompt: str):
    while 1:
        for model_name in MODELS:
            wait = 8
            for i in range(1, max_tries + 1):
                try:
                    print("trying model %s ... %s/%s" % (model_name, i, max_tries), flush=True)
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    return response.text
                except APIError as e:
                    if e.code in (429, 503):
                        wait *= 2
                        template = f"{model_name} busy ({e.code}). [sleep %s]."
                        sleep(wait, template=template)
                    else:
                        raise

