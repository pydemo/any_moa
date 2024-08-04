import os, time
import asyncio

from anthropic import AsyncAnthropic, RateLimitError
from include.common import get_final_system_prompt
from pprint import pprint as pp



class AsyncClient(AsyncAnthropic):   
    def __init__(self, api_key):
        super().__init__(api_key=api_key)

async def get_final_stream(client,aggregator_model,user_prompt,  results):
    sys_prompt = get_final_system_prompt( results)
    for sleep_time in [1, 2, 4]:
        try:


            async with client.messages.stream(
                 model=aggregator_model,
                max_tokens=1024,
                system=sys_prompt,
                messages=[
             
                    {"role": "user", "content": user_prompt},
                ],
            ) as final_stream:
                async for text in final_stream.text_stream:
                    yield text
            break

        except RateLimitError as e:
            print(e)
            await asyncio.sleep(sleep_time)   




async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:  anthropic: run_llm:', model)
    sys_prompt = None
    if prev_response:
        sys_prompt = get_final_system_prompt(  prev_response)
        #pp(sys_prompt)

    for sleep_time in [1, 2, 4]:
        try:
            system={'system':sys_prompt}   if prev_response else {}
            messages = (
                [

                    {"role": "user", "content": user_prompt},
                ]
                if prev_response
                else [{"role": "user", "content": user_prompt}]
            )
            #pp(messages)
            response = await client.messages.create(
                model=model,
                **system,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )


            

            print(f"\t\t{layer}:     groq: Sleep: {sleep_time}: Model: ", model)
            break
        except RateLimitError as e:
            print(e)
            await asyncio.sleep(sleep_time)
    assert response.content
    print(f'\t  {layer}:','anthropic'.rjust(10,' '),f':{model}:Content:', len(response.content), response.content[0].text[:50])
    return response.content[0].text