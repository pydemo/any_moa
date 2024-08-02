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
e=sys.exit


clients={}
def get_client (api):
    global clients
    if api not in clients:
        client_api = globals()[api].AsyncClient
        api_key = os.getenv(f"{api.upper()}_API_KEY")
        assert api_key, f"API key for {api_key} not found"
        clients[api] =  client_api(api_key)

    return clients[api]
    
def close_clients():
    global clients
    for client in clients.values():
        client.close()

@click.command()
@click.argument('yaml_file_path', type=click.Path(exists=True))
def main(yaml_file_path):
    async def async_main():
        """Run the main loop of the MOA process."""
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)

        reference_models = data['reference_models']
        layers = 3

        aggregator_model = next((model['name'] for model in data['reference_models'] if model.get('aggregator')), None)
        aggregator_api = next((model['api'] for model in data['reference_models'] if model.get('aggregator')), None)
        print(f"Aggregator API: {aggregator_api}")
        print(f"Aggregator model: {aggregator_model}")
        print("Running main loop...")
        try:
            apis = [dict(run=getattr(globals()[model['api']], 'run_llm'), model=model['name'], api=model['api']) for model in reference_models]
            pp(apis)
            results = await asyncio.gather(*[api['run'](get_client(api['api']), 0, api['model']) for api in apis])
            print("Running layers...")
            for i in range(1, layers - 1):
                print(f"Layer {i}")
                results = await asyncio.gather(*[api['run'](get_client(api['api']), 0, api['model'], prev_response=results) for api in apis])

            print("Final layer")
            final_stream_api = globals()[aggregator_api].get_final_stream
            async for chunk in final_stream_api(get_client(aggregator_api), aggregator_model,results):
                if chunk:
                    print(chunk, end='', flush=True)
        finally:
            close_clients
    asyncio.run(async_main())
if __name__ == "__main__":
    main()
