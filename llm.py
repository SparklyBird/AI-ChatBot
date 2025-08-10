import copy
import spacy

nlp = spacy.load('en_core_web_lg')


def run_model_with_prompt(llm, text_prompt):
    # A more detailed prompt to guide the model's response style
    prompt = f"""SYSTEM: You are a helpful assistant. Provide a concise, direct answer.
USER: {text_prompt}
ASSISTANT:"""

    try:
        stream = llm(
            prompt,
            max_tokens=512,  # Increased token limit
            stop=["USER:", "\n\n"],  # Better stopping criteria
            stream=True
        )
        output_text = ""
        for output in stream:
            completionFragment = copy.deepcopy(output)
            output_text += completionFragment["choices"][0]["text"]
        return output_text.strip()  # Cleaned up output
    except Exception as e:
        print("Error executing model:", str(e))