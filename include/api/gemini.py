
import os, sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
from include.common import get_final_system_prompt
from pprint import pprint as pp

import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory
)
e=sys.exit


LOCATION = "us-central1"




    
class AsyncClient:
          
    def __init__(self, api_key):
        self.project_id = api_key
        self.model=None
        self.contents=None
        self.session = None
        vertexai.init(project=api_key, location=LOCATION)

        self.generation_config = GenerationConfig(
            temperature=0.7,
            max_output_tokens=1024,
            top_p=0.8,
            top_k=40,
            candidate_count=1,
        )

        # Set safety settings
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }        
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
        system_instruction={}
        sys_prompt = None
        if prev_response:
            sys_prompt = get_final_system_prompt(  prev_response)
            system_instruction = {'system_instruction':[sys_prompt]}



        # Load a example model with system instructions
        #MODEL_ID = 'gemini-pro'  # @param {type:"string"}
        #pp(system_instruction)
        self.model = GenerativeModel(
            model_id,
            **system_instruction
        )


        
        prompt = f"""
        User input: {user_prompt}
        Answer:
        """

        # Set contents to send to the model
        self.contents = [prompt]

        # Counts tokens
        #print(self.model.count_tokens(self.contents))

        output = await self.generate_content_async()
        #print(output)
        
        return output

    async def generate_content_async(self):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, self.generate_content_sync)
        return result    
    def generate_content_sync(self):
        assert self.model
        assert self.contents    
        # Set model parameters


        response = self.model.generate_content(
            self.contents,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=False,  # Ensure streaming is disabled
        )
        return response.text  # Access the text attribute directly            


    async def stream_content(self, model, contents):
        stream = await model.generate_content_async(
            contents,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=True,
        )
        
        async for chunk in stream:
            yield chunk.text

async def get_final_stream(client,aggregator_model,user_prompt,  results):
    sys_prompt = get_final_system_prompt( results)

    system_instruction = {'system_instruction':[sys_prompt]}



    # Load a example model with system instructions
    #MODEL_ID = 'gemini-pro'  # @param {type:"string"}
    #pp(system_instruction)
    model = GenerativeModel(
        aggregator_model,
        **system_instruction
    )


    
    prompt = f"""
    User input: {user_prompt}
    Answer:
    """

    # Set contents to send to the model
    contents = [prompt]
    
    #print(model.count_tokens(contents))

    async for chunk in client.stream_content(model, contents):
        yield chunk
    
    


async def run_llm(client, layer, model, user_prompt,prev_response=None):
    """Run a single LLM call with a model while accounting for previous responses + rate limits."""
    print(f'\t{layer}:     gemini: run_llm:', model)

    
    response = await client.chat(
        model_id=model,
        user_prompt=user_prompt,
        prev_response=prev_response
        #temperature=0.7,
        # max_tokens=512,
    )
    #print(f"\t\t{layer}:     openai: Sleep: {sleep_time}: Model: ", model)
    
    
    
    content = response
    
    assert content
    

    
    print(f'\t  {layer}:','gemini'.rjust(10,' '),f':{model}:Content:', len(content))
    return content