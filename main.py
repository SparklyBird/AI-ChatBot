from dotenv import load_dotenv
import os

# Get an API key that is getting used
load_dotenv(override=True)
# The debug print for the API key can be removed for the final version
# print(f"--- DEBUG: API Key Loaded: {os.getenv('ELEVEN_API_KEY')} ---")

import logging
import warnings
# Suppress harmless warnings for a cleaner console
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Silence verbose logs from noisy libraries
logging.getLogger("parler_tts").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("comtypes").setLevel(logging.WARNING) # Added to hide comtypes info logs

import spacy
from llama_cpp import Llama
from bot import bot

# --- Main Application Entry Point ---
if __name__ == '__main__':
    # Suppress harmless warnings for a cleaner console
    warnings.filterwarnings('ignore', category=UserWarning)
    logging.getLogger("transformers").setLevel(logging.ERROR)
    llm = None
    nlp = None
    # Load models
    try:
        print("Loading spaCy NLP model...")
        nlp = spacy.load('en_core_web_lg')
        print("spaCy model loaded!")
        print("Loading LLM model...")
        llm = Llama(
            model_path="./models/WizardLM-13B-Uncensored.Q5_K_M.gguf",
            n_gpu_layers=-1,
            n_ctx=2048,
            verbose=False
        )
        print("LLM Model loaded!")
    except Exception as e:
        print(f"Error loading models: {e}")
    # Start the bot if models loaded successfully
    if llm and nlp:
        try:
            print("\nBot is running. Press Ctrl+C to exit.")
            bot(llm, nlp)
        except KeyboardInterrupt:
            print("\n\nBot stopped. Goodbye!")