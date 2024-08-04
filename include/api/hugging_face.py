
import os, sys, re
import aiohttp
import asyncio
from huggingface_hub import AsyncInferenceClient
from include.common import get_final_system_prompt
from pprint import pprint as pp
e=sys.exit



    
class AsyncClient(AsyncInferenceClient):
    def __init__(self, api_key):
        
        super().__init__( token=api_key)    

    async def chat(self, model, messages):
        response = await self.chat_completion(messages, max_tokens=500)
        
        return response
            
    def close(self) -> None:
        pass

async def get_final_stream(client,aggregator_model,user_prompt,  results):
    sys_prompt = get_final_system_prompt( results)

    
    

    messages=[
        {
            "role": "system",
            "content": sys_prompt,
        },
        {"role": "user", "content": user_prompt},
    ]
    response = await client.chat_completion(messages, max_tokens=500)
    yield  response.choices[0].message.content
    if 0:
        async for token in await client.chat_completion(messages, model=aggregator_model, max_tokens=500, stream=True):
            content=token.choices[0].delta.content
            if content:
                yield content
    


async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:hugging_face: run_llm:', model)
    sys_prompt = None
    if prev_response:
        sys_prompt = get_final_system_prompt(  prev_response)
        #pp(sys_prompt)

    messages = (
        [
            {
                "role": "system",
                "content": sys_prompt,
            },
            {"role": "user", "content": user_prompt},
        ]
        if prev_response
        else [{"role": "user", "content": user_prompt}]
    )
    
    response = await client.chat(
        model=model,
        messages=messages, 
        #temperature=0.7,
        # max_tokens=512,
    )
    #print(f"\t\t{layer}:     openai: Sleep: {sleep_time}: Model: ", model)
    
    
    
    content = response.choices[0].message.content
    
    assert content
    

    
    print(f'\t  {layer}:','hugging_face'.rjust(10,' '),f':{model}:Content:', len(content))
    return content