import os
import asyncio
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel

# Initialize Vertex AI
aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

def predict_large_language_model_sample(
    project_id: str,
    model_name: str,
    temperature: float,
    max_output_tokens: int,
    top_p: float,
    top_k: int,
    location: str = "us-central1",
):
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)

    chat_model = ChatModel.from_pretrained(model_name)
    parameters = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "top_p": top_p,
        "top_k": top_k,
    }

    chat = chat_model.start_chat(examples=[])
    response = chat.send_message("What version of PaLM are you?", **parameters)
    return response.text

async def main():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    model_name = "chat-bison@001"
    location = "us-central1"  # You can change this if needed
    
    try:
        response = predict_large_language_model_sample(
            project_id=project_id,
            model_name=model_name,
            temperature=0,
            max_output_tokens=256,
            top_p=0.8,
            top_k=40,
            location=location
        )
        print("Response:")
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())