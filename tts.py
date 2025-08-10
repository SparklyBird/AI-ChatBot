import os
import re
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# --- Comprehensive Unit and Symbol Dictionary ---
# This dictionary will be used to replace symbols and abbreviations with full words.
NORMALIZATION_MAP = {
    # Symbols
    "-": "minus ",
    "²": " square",
    "³": " cubic",
    # Length & Distance
    "km/h": "kilometers per hour", "m/s": "meters per second", "mph": "miles per hour",
    "km": "kilometers", "cm": "centimeters", "mm": "millimeters", "mi": "miles", "ft": "feet", "in": "inches",
    "m": "meters",
    # Area
    "ha": "hectares", "acre": "acres",
    # Volume
    "mL": "milliliters", "US gal": "U.S. gallons", "UK gal": "U.K. gallons", "L": "liters",
    # Mass / Weight
    "kg": "kilograms", "lb": "pounds", "oz": "ounces", "g": "grams", "t": "tonnes",
    # Time
    "min": "minutes", "hr": "hours", "yr": "years", "s": "seconds", "h": "hours", "d": "days",
    # Temperature
    "°C": " degrees Celsius", "°F": " degrees Fahrenheit", "K": " kelvin",
    # Others
    "kt": "knots", "Pa": "pascals", "psi": "pounds per square inch", "bar": "bar",
    "J": "joules", "kJ": "kilojoules", "kcal": "kilocalories", "kWh": "kilowatt-hours",
    "W": "watts", "kW": "kilowatts", "hp": "horsepower",
    "KB": "kilobytes", "MB": "megabytes", "GB": "gigabytes", "b": "bits", "B": "bytes",
}

def normalize_text_for_tts(text: str) -> str:
    # Cleans up text for better TTS pronunciation by expanding symbols and units.
    # Remove commas from inside numbers (e.g., "6,371" -> "6371")
    # ElevenLabs reads the resulting number correctly.
    text = re.sub(r'(?<=\d),(?=\d)', '', text)
    # Use the dictionary to replace units and symbols, longest ones first
    for unit, full_name in sorted(NORMALIZATION_MAP.items(), key=lambda item: len(item[0]), reverse=True):
        # Using word boundaries (\b) for some units to avoid replacing parts of words
        if unit.isalpha():
            text = re.sub(r'\b' + re.escape(unit) + r'\b', f" {full_name}", text)
        else:
            text = text.replace(unit, full_name)
    return text.strip()

# For the ElevenLabs API
client = None
try:
    print("Initializing ElevenLabs TTS client...")
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY not found in environment or .env file.")
    client = ElevenLabs(api_key=api_key)
    print("ElevenLabs client initialized!")
except Exception as e:
    print(f"Could not initialize ElevenLabs client.")
    print(f"Error details: {e}")

def convert_text_to_speech(text: str):
    #Converts text to speech using the ElevenLabs API and plays it automatically.
    if not client:
        print("TTS client is not initialized. Cannot play audio.")
        return
    try:
        # Normalize the text before sending it to the API ---
        normalized_text = normalize_text_for_tts(text)
        audio = client.text_to_speech.convert(
            text=normalized_text,
            voice_id="EXAVITQu4vr4xnSDxMaL"
            # Bella: EXAVITQu4vr4xnSDxMaL (Good, regular voice)
            # Matilda: XrExE9yKIg1WjnnlVkGX (Good, regular voice)
            # Josh: TxGEqnHWrfWFTfGW9XjX (Good, regular voice)
            # Matthew: Yko7PKHZNXotIFUBG7I9 (Elegant dude)
            # Fin: D38z5RcWu1voky8WS1ja (Funny guy)
            # Gigi: jBpfuIE2acCO8z3wKNLl (Energetic girl)
            # Glinda: z9fAnlkpzviPz146aGWa (Mommy)
            # Nicole: piTKgcLEGmPE4e6mEKli (ASMR)
            # Patrick: ODq5zmih8GrVes37Dizd (Loud dude like some knight)
        )
        play(audio)
    except Exception as e:
        print(f"Error converting text-to-speech with ElevenLabs: {e}")