import os
import requests

# Define the API token and URL

HUGGING_FACE_TOKEN = os.getenv(f"HUGGING_FACE_TOKEN")

import requests

def query(payload, model_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

model_id = "facebook/blenderbot-400M-distill"  # Change to your desired model ID
model_id = "HuggingFaceH4/zephyr-7b-beta"
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
model_id = "mistralai/Mistral-7B-v0.1"

#model from Hugginf Face
model_id = "mistralai/Mistral-Nemo-Instruct-2407"
model_id = "HuggingFaceTB/SmolLM-135M"
model_id = "microsoft/Phi-3-mini-4k-instruct"


# Define the input data and parameters
api_token = HUGGING_FACE_TOKEN
data = query({"inputs": "Hello! List  top things to do in Jersey City?"}, model_id, api_token)
print(data)
