# Advanced AI Voice Chatbot

This project is a sophisticated, command-line conversational AI that leverages a local Large Language Model (LLM) for reasoning and the ElevenLabs API for high-quality, real-time voice synthesis. It features a persistent memory system backed by a SQLite database, allowing it to learn and recall previous conversations using semantic search.

This chatbot is designed to run on a local machine with GPU acceleration for fast and efficient LLM inference.

## Features

-   **Local LLM Inference:** Utilizes `llama-cpp-python` to run powerful GGUF-format language models (e.g., WizardLM, Mistral) locally with full GPU offloading.
-   **High-Quality, Real-Time TTS:** Integrates with the **ElevenLabs API** to provide natural, studio-quality voice responses with minimal latency.
-   **Persistent Memory:** Remembers past questions and answers in a SQLite database (`memory.db`), allowing it to learn over time.
-   **Semantic Search:** Employs `spaCy`'s language models to find answers to semantically similar questions in its memory, rather than just exact matches.
-   **Asynchronous Audio:** The bot responds instantly with text in the console while the audio is generated and played in the background, creating a highly responsive user experience.
-   **Advanced Text Normalization:** A custom pre-processing step expands abbreviations (e.g., "km"), symbols (e.g., "-"), and special characters (e.g., "²") into full words for clear and accurate pronunciation.

## Technology Stack

-   **Language:** Python 3.12
-   **LLM Backend:** `llama-cpp-python`
-   **TTS Backend:** ElevenLabs API
-   **NLP / Search:** `spaCy`
-   **Database:** SQLite

---

## Setup and Installation

Follow these steps to set up and run the project.

### 1. Prerequisites

-   **Python 3.12 (64-bit)** installed and added to your system's PATH.
-   An **NVIDIA GPU** with a compatible **CUDA Toolkit** installed (the project was built with CUDA 12.1).
-   **Git** for cloning the repository.
-   **Visual Studio Build Tools** with the "Desktop development with C++" workload (required for `llama-cpp-python` compilation).

### 2. Clone the Repository
```bash
git clone [https://github.com/SparklyBird/AI-ChatBot.git](https://github.com/SparklyBird/AI-ChatBot.git)
cd AI-ChatBot