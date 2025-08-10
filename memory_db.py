import sqlite3

DATABASE_FILE = 'memory.db'

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY,
                        question TEXT UNIQUE,
                        answer TEXT,
                        processed_info TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to save a single entry
# Note: The nlp object is passed from llm.py via bot.py
def save_single_memory_entry(question: str, answer: str, nlp):
    """Saves a single question-answer pair to the database."""
    processed_question = question.strip().capitalize()
    if not processed_question.endswith('?'):
        processed_question += '?'
    doc = nlp(processed_question)
    processed_info = ' '.join([token.lemma_ for token in doc if token.pos_ in {'VERB', 'ADJ', 'NOUN', 'NUM'}])
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO memory (question, answer, processed_info) VALUES (?, ?, ?)",
            (processed_question, answer, processed_info)
        )