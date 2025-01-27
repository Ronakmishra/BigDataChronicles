import openai
from dotenv import load_dotenv
import os
import jsonlines
import pandas as pd
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load metadata from JSONL file
def load_metadata(file_path):
    """Load metadata from a JSONL file."""
    with jsonlines.open(file_path) as reader:
        return [obj for obj in reader]

# Get OpenAI response using the updated ChatCompletion API
def get_openai_response(context, question):
    """Send context and question to OpenAI and get the response."""
    # Format messages for the Chat API
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context: {context}\nQuestion: {question}\nAnswer:"}
    ]

    # Call the ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if desired
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )

    # Extract and return the assistant's response
    return response.choices[0].message.content.strip()

# Save feedback to JSONL file
def save_feedback(test_case_id, response, feedback):
    """Save user feedback for a test case."""
    entry = {
        "test_case_id": test_case_id,
        "response": response,
        "feedback": feedback
    }
    with open("feedback.jsonl", "a") as f:
        jsonlines.Writer(f).write(entry)

# Compare OpenAI response with the ground truth
def compare_answers(response, ground_truth):
    """Compare the OpenAI response with the ground truth answer."""
    # Normalize and compare answers
    return response.strip().lower() == ground_truth.strip().lower()

# Visualize feedback as a chart
def visualize_feedback():
    """Visualize feedback summary using a bar chart."""
    try:
        feedback_data = pd.read_json("feedback.jsonl", lines=True)
        st.bar_chart(feedback_data["feedback"].value_counts())
    except Exception as e:
        st.error("No feedback data available yet.")
