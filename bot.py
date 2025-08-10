import textwrap
import threading
from similarity import get_answer_based_on_similarity
from tts import convert_text_to_speech
from llm import run_model_with_prompt
from memory_db import DATABASE_FILE, create_table, save_single_memory_entry

def speak(text):
    """Helper function to run TTS in a separate, non-blocking thread."""
    convert_text_to_speech(text)

def bot(llm, nlp):
    """Main chatbot loop."""
    create_table()
    while True:
        user_input = input('\nUser: ')
        if user_input.lower() == 'quit':
            break
        final_answer = ""
        answer_from_memory = get_answer_based_on_similarity(user_input, nlp, DATABASE_FILE)
        if answer_from_memory:
            final_answer = answer_from_memory
        else:
            llm_answer = run_model_with_prompt(llm, user_input)
            save_single_memory_entry(user_input, llm_answer, nlp)
            final_answer = llm_answer
        cleaned_answer = final_answer.strip()
        print(f"Bot: {cleaned_answer}")
        # Start speech synthesis in the background
        tts_thread = threading.Thread(target=speak, args=(cleaned_answer,))
        tts_thread.start()