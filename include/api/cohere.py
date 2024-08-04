import os, time
import asyncio
import groq
import cohere
from include.common import get_final_system_prompt
from pprint import pprint as pp

import include.config.init_config as init_config 

init_config.init(**{})
apc = init_config.apc


class AsyncClient(cohere.AsyncClient):   
    def __init__(self, api_key):
        super().__init__(api_key=api_key)
    async def close(self):
        pass       

async def get_final_stream(client,aggregator_model,user_prompt,  results):
    sys_prompt = {'preamble':get_final_system_prompt(  results)}


    web_search = {}
    is_ws=apc.models[aggregator_model].get('web_search',False)
    if is_ws:
        web_search = {"connectors":[{"id": "web-search"}]}

    final_stream = client.chat_stream(
        model=aggregator_model,
        message= user_prompt,
        **sys_prompt,
        max_tokens=300 ,
        **web_search
       
    )
    out=[]
    async for event in final_stream:
        if event.event_type == "text-generation":
            text= event.text
            out.append(text)
            yield  text
        elif event.event_type == "stream-end":
            print(event.finish_reason)
    print(f'Aggregator :','cohere'.rjust(10,' '),f': {aggregator_model}: web_search: {is_ws}: Content:', len(' '.join(out)))  

async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:    cohere: run_llm:', model)
    sys_prompt = {}
    if prev_response:
        sys_prompt = {'preamble':get_final_system_prompt(  prev_response)}
    web_search = {}
    is_ws=apc.models[model].get('web_search',False)
    if is_ws:
        web_search = {"connectors":[{"id": "web-search"}]}
    
    response = await client.chat(
        model=model,
        message  = user_prompt,
        **sys_prompt,
        max_tokens=300 ,
        **web_search
    )
    

   
    text=response.text
   
    print(f'\t  {layer}:','cohere'.rjust(10,' '),f': {model}: web_search: {is_ws}: Content:', len(text))
    return text




