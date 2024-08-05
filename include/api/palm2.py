
import os, sys
import asyncio
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel, TextGenerationModel
from include.common import get_final_system_prompt
from pprint import pprint as pp


e=sys.exit


LOCATION = "us-central1"

    
class AsyncClient:
          
    def __init__(self, api_key):
        self.project_id = api_key
        self.model=None
        self.contents=None
        self.session = None
        #aiplatform.init(project=self.project_id)
        vertexai.init(project=self.project_id, location=LOCATION)
       
    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    async def initialize(self):
        if self.session is None:
            self.session = 1
            


    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None    

    async def chat(self, model_id,user_prompt,  prev_response):
        
        sys_prompt = ''
        if prev_response:
            sys_prompt = get_final_system_prompt(  prev_response)
            

        temperature=0
        max_output_tokens=256
        top_p=0.8
        top_k=40

        chat_model = ChatModel.from_pretrained(model_id)
        parameters = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_p": top_p,
            "top_k": top_k,
        }

        # Set the system message
        system_message = sys_prompt 

        chat = chat_model.start_chat(context=system_message)
        response = await asyncio.to_thread(chat.send_message,user_prompt, **parameters)
        return response.text

    async def text(self, model_id,user_prompt,  prev_response):
        
        sys_prompt = ''
        if prev_response:
            sys_prompt = get_final_system_prompt(  prev_response)
            

        temperature=0
        max_output_tokens=256
        top_p=0.8
        top_k=40

        model = TextGenerationModel.from_pretrained(model_id)
        parameters = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_p": top_p,
            "top_k": top_k,
        }

   

        prompt = f"{sys_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"
        response = await asyncio.to_thread(model.predict,prompt, **parameters)
        return response.text

    async def streaming_chat(self,aggregator_model,user_prompt,  results):
        sys_prompt = get_final_system_prompt( results)

    

        chat_model = ChatModel.from_pretrained(aggregator_model)


        temperature=0
        max_output_tokens=256
        top_p=0.8
        top_k=40
        
        parameters = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_p": top_p,
            "top_k": top_k,
        }

        system_message = sys_prompt

        chat = chat_model.start_chat(context=system_message)
        responses = chat.send_message_streaming(
        user_prompt, **parameters
        )
        

        for response in responses:
            yield response.text

    async def streaming_text(self,aggregator_model,user_prompt,  results):
        sys_prompt = get_final_system_prompt( results)

    

        model = TextGenerationModel.from_pretrained(aggregator_model)


        temperature=0
        max_output_tokens=256
        top_p=0.8
        top_k=40
        
        parameters = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_p": top_p,
            "top_k": top_k,
        }

        

        prompt = f"{sys_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"
        stream = await asyncio.to_thread(model.predict_streaming, prompt, **parameters)
    

        for response in stream:
            chunk = response.text
            yield chunk

    
            
    def close(self) -> None:
        pass



async def get_final_stream(client,aggregator_model,user_prompt,  results):
    
    if aggregator_model.startswith('chat'):
        async for response in client.streaming_chat(aggregator_model,user_prompt,  results):
            yield response
    else:
        async for response in client.streaming_text(    aggregator_model,user_prompt,  results):
            yield response
        
    

    


async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:      palm2: run_llm:', model)

    if model.startswith('chat'):
        response = await client.chat(
            model_id=model,
            user_prompt=user_prompt,
            prev_response=prev_response
            #temperature=0.7,
            # max_tokens=512,
        )
    else:
        response = await client.text(
            model_id=model,
            user_prompt=user_prompt,
            prev_response=prev_response
            #temperature=0.7,
            # max_tokens=512,
        )
  
    
    
    
    content = response
    
    assert content
    

    
    print(f'\t  {layer}:','palm2'.rjust(10,' '),f':{model}:Content:', len(content))
    return content