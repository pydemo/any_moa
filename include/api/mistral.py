
import os
import aiohttp
import asyncio
from include.common import get_final_system_prompt
from pprint import pprint as pp

class RateLimitError(Exception):
    pass

class AsyncClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat(self, model, messages):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 429:  # HTTP status code for Too Many Requests
                    raise RateLimitError("Rate limit exceeded. Please wait before making another request.")
                elif response.status != 200:
                    raise Exception(f"Chat API request failed: {response.status} {await response.text()}")
                return await response.json()
            


async def get_final_stream(client,aggregator_model,user_prompt,  results):
    sys_prompt = get_final_system_prompt( results)

    messages=[
        {
            "role": "system",
            "content": sys_prompt,
        },
        {"role": "user", "content": user_prompt},
    ]
   
    

    url = f"{client.base_url}/chat/completions"
    payload = {
        "model": aggregator_model,
        "messages": messages
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=client.headers, json=payload) as response:
            if response.status == 429:  # HTTP status code for Too Many Requests
                raise RateLimitError("Rate limit exceeded. Please wait before making another request.")
            elif response.status != 200:
                content=await response.json()
                pp(content)

                raise Exception(f"Chat AP I request failed: {response.status} ")
            content=await response.json()
            #pp(content)
            out=content['choices'][0]['message']['content']
            assert out
            yield out
            
    

async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:    mistral: run_llm:', model)
    sys_prompt = None
    if prev_response:
        sys_prompt = get_final_system_prompt(  prev_response)
        #pp(sys_prompt)

    for sleep_time in [1, 2, 4]:
        try:
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
            break
        except RateLimitError as e:
            print(e)
            await asyncio.sleep(sleep_time)
    content = response['choices'][0]['message']['content']
    assert content
    
    print(f'\t  {layer}:','mistral'.rjust(10,' '),f':{model}:Content:', content[:50])
    return content