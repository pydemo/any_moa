import os, sys
import asyncio
import yaml 
import click
from pprint import pprint as pp
from os.path import join
#from  include.api.deepinfra import AsyncClient, get_final_stream
import include.api.deepinfra as deepinfra
import include.api.groq as groq
import include.api.together as together
import include.api.openai as openai 
import include.api.mistral as mistral
import include.api.nvidia as nvidia
import include.api.deepseek as deepseek
import include.api.hugging_face as hugging_face
import include.api.anthropic as anthropic
import include.api.gemini as gemini
import include.api.cohere as cohere
import include.api.palm2 as palm2
from include.common import get_aggregator 
e=sys.exit

import include.config.init_config as init_config 

init_config.init(**{})
apc = init_config.apc
apc.models={}
clients={}

def get_client (api):
    global clients
    if api not in clients:
        client_api = globals()[api].AsyncClient
        api_key = os.getenv(f"{api.upper()}_API_KEY")
        assert api_key, f"API key for '{api}' not found"
        clients[api] =  client_api(api_key)

    return clients[api]

       
def close_clients():
    global clients
    for client in clients.values():
        client.close()

def save_models(reference_models):    
    for x in reference_models:
        model_id=x['name']
        assert model_id not in apc.models
        apc.models[model_id]=x

@click.command()
@click.argument('yaml_file_path', type=click.Path(exists=True))
@click.argument('num_of_layers', type=int, default=3)
def main(yaml_file_path, num_of_layers):
    async def async_main():
        """Run the main loop of the MOA process."""
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)

        if reference_models := data.get('reference_models', None  ):
            save_models(reference_models)
        else:
            print('No reference models found')
            assert num_of_layers==1, 'num_of_layers for aggregator only pipeline should be 1'

        aggregator_model, aggregator_api = get_aggregator(data) 
        print(f"Aggregator API: {aggregator_api}")
        print(f"Aggregator model: {aggregator_model}")
        
        print("Running main loop...")
        try:
            while True:
                print()
                default_prompt="What is 42?"
                user_prompt = input(f"Enter your prompt ({default_prompt}): ")
                if not user_prompt:
                    user_prompt = default_prompt
                
                if num_of_layers>1:

                    assert reference_models
                    apis = [dict(run=getattr(globals()[model['api']], 'run_llm'), model=model['name'], api=model['api']) for model in reference_models]
                    print('Layer 0')
                    results = await asyncio.gather(*[api['run'](get_client(api['api']), 0, api['model'], user_prompt) for api in apis])
                    print("Running layers...")
                    for i in range(1, num_of_layers - 1):
                        print(f"Layer {i}")
                        results = await asyncio.gather(*[api['run'](get_client(api['api']), i, api['model'],user_prompt, prev_response=results) for api in apis])
                else:
                    #go aggregator directly
                    results={}

                print(f"Final layer (Aggregator: {aggregator_api}: {aggregator_model})")
                print()
                final_stream_api = globals()[aggregator_api].get_final_stream
                async for chunk in final_stream_api(get_client(aggregator_api), aggregator_model,user_prompt,results):
                    if chunk:
                        print(chunk, end='', flush=True)
                print()
        finally:
            close_clients()
    asyncio.run(async_main())
if __name__ == "__main__":
    main()
