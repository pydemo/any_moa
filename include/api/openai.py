import os, time
import asyncio
import openai
from openai import AsyncOpenAI
from include.common import get_final_system_prompt
from pprint import pprint as pp




class AsyncClient(AsyncOpenAI):   
    def __init__(self, api_key):
        super().__init__(api_key=api_key)

async def get_final_stream(client,aggregator_model,user_prompt,  results):
    sys_prompt = get_final_system_prompt( results)
    
    final_stream = await client.chat.completions.create(
        model=aggregator_model,
        messages=[
            {
                "role": "system",
                "content": sys_prompt,
            },
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )
    async for chunk in final_stream:
        yield chunk.choices[0].delta.content or ""
    

async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:    openai: run_llm:', model)
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
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=512,
            )
            #print(f"\t\t{layer}:     openai: Sleep: {sleep_time}: Model: ", model)
            break
        except openai.RateLimitError as e:
            print(e)
            await asyncio.sleep(sleep_time)
    assert response.choices[0].message.content
    print(f'\t  {layer}:','openai'.rjust(10,' '),':{model}:Content:', response.choices[0].message.content[:50])
    return response.choices[0].message.content