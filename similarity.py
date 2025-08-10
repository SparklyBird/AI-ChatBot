import sqlite3
import re


def clean_text(text: str) -> str:
    # A helper function to standardize question text for exact matching.
    # Remove all non-alphanumeric characters (except spaces) and lowercase
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).lower().strip()

def get_answer_based_on_similarity(question: str, nlp, database_file: str) -> str | None:
    """
    Finds the best answer from the database.
    First, it checks for an exact match. If none is found, it then
    checks for semantic similarity using spaCy.
    """
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM memory")
        rows = cursor.fetchall()
    if not rows:
        return None
    cleaned_user_question = clean_text(question)
    # --- Step 1: Check for an EXACT match first ---
    for db_question_str, db_answer in rows:
        if clean_text(db_question_str) == cleaned_user_question:
            # The "exact match" print statement has been removed from here.
            return db_answer
    # --- Step 2: If no exact match, check for a SIMILAR match ---
    question_doc = nlp(question)
    if not question_doc.has_vector or not question_doc.vector_norm:
        return None
    best_match_answer = None
    highest_similarity = 0.95
    for db_question_str, db_answer in rows:
        db_doc = nlp(db_question_str)
        if db_doc.has_vector and db_doc.vector_norm:
            similarity_score = question_doc.similarity(db_doc)
            if similarity_score > highest_similarity:
                highest_similarity = similarity_score
                best_match_answer = db_answer
    # The "similar match" print statement has also been removed.
    return best_match_answer