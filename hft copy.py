import os
import requests

# Define the API token and URL

HUGGING_FACE_TOKEN = os.getenv(f"HUGGING_FACE_TOKEN")
API_URL = "https://api-inference.huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct"

# Define the headers with the Authorization token
headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}

# Function to query the API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Define the input data and parameters
data = {
    "inputs": "What's the capical of france?",
    "parameters": {"do_sample": False}
}

# Query the API and get the response
response = query(data)

# Print the response
print(response)
