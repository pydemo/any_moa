import os, time
import together
import asyncio
from together import AsyncTogether 
from together import  Together
from include.common import get_final_system_prompt
from pprint import pprint as pp


class AsyncClient(AsyncTogether):
    def __init__(self, api_key):
        self.api_key = api_key
        #self.connector = TCPConnector(ssl=True)
        self.session = None
        super().__init__(api_key=api_key)
    async def __aenter__(self):
        #await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


    async def close(self):
        if self.session:
            del self.session
            self.session = None

async def get_final_stream(client, aggregator_model,user_prompt, results):
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

async def run_llm(client, layer, model,user_prompt, prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:  together: run_llm:', model)
    sys_prompt = None
    if prev_response:
        sys_prompt = get_final_system_prompt( prev_response)
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
            print(f"\t\t{layer}: together: Sleep: {sleep_time}: Model: ", model)
            break
        except together.error.RateLimitError as e:
            print(e)
            await asyncio.sleep(sleep_time)
    assert response.choices[0].message.content
    print(f'\t  {layer}:','together'.rjust(10,' '),f':{model}:Content:', response.choices[0].message.content[:50])
    return response.choices[0].message.content