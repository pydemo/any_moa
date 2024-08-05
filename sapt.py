import os
import asyncio
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

# Initialize Vertex AI
aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

async def predict_large_language_model_sample_streaming(
    project_id: str,
    model_name: str,
    temperature: float,
    max_output_tokens: int,
    top_p: float,
    top_k: int,
    location: str = "us-central1",
):
    """Predict using a Large Language Model with streaming."""
    vertexai.init(project=project_id, location=location)

    chat_model = ChatModel.from_pretrained(model_name)
    parameters = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "top_p": top_p,
        "top_k": top_k,
    }

    system_message = "You are an AI assistant created by Google. Your name is Claude and you were trained by Anthropic, PaLM."

    chat = chat_model.start_chat(context=system_message)
    responses = chat.send_message_streaming(
        "What version of PaLM are you?", **parameters
    )
    
    full_response = ""
    for response in responses:
        print(response.text, end="", flush=True)
        full_response += response.text
    
    print()  # New line after the full response
    return full_response

async def main():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    model_name = "chat-bison@001"
    location = "us-central1"  # You can change this if needed
    
    try:
        print("Streaming Response:")
        response = await predict_large_language_model_sample_streaming(
            project_id=project_id,
            model_name=model_name,
            temperature=0,
            max_output_tokens=256,
            top_p=0.8,
            top_k=40,
            location=location
        )
        print("\nFull Response:")
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())