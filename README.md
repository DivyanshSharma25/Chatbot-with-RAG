# LLM with RAG

This project implements a version of Retrieval-Augmented Generation (RAG) using Large Language Models (LLMs). The goal is to enhance the retrieval and generation process for improved performance in various natural language processing tasks.

## Features

- **Custom Retrieval Mechanism**: Optimized for domain-specific data.
- **Enhanced Generation**: Fine-tuned LLM for better contextual responses.
- **Scalable Architecture**: Designed to handle large datasets efficiently.
- **Modular Design**: Easy to extend and customize.

## Prerequisites

- Python 3.8 or higher
- Required libraries listed in `requirements.txt`
- Access to a pre-trained LLM model (e.g., OpenAI GPT, Hugging Face models)
- Ollama installed on your machine along with the model you are using

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/llm-with-rag.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask application:

   ```bash
   python app.py
   ```

4. Navigate to `http://127.0.0.1:5000` in your web browser to access the application.

## Usage

1. Open the application in your web browser.
2. Upload a PDF or DOC file using the upload field on the webpage.
3. Ask questions in the chatbot interface. The chatbot will respond based on the information provided in the uploaded file.
