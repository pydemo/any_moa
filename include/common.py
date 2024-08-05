import os
aggregator_system_prompt = """You have been provided with a set of responses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""



def get_final_system_prompt( results):
    global aggregator_system_prompt
    """Construct a system prompt for layers 2+ that includes the previous responses to synthesize."""
    return (
        aggregator_system_prompt
        + "\n"
        + "\n".join([f"{i+1}. {str(element)}" for i, element in enumerate(results)])
    )


def get_aggregator(data):
    if 'aggregator' in data:
        if reference_models := data.get('reference_models', None  ):
            reference_aggregator_model = next((model['name'] for model in data['reference_models'] if model.get('aggregator')), None)
            assert reference_aggregator_model is None, f"Ignoring aggregator defined in reference_models: {reference_aggregator_model}"
        assert len(data['aggregator'])==1, f"Only one aggregator model is supported"
        aggregator_model = data['aggregator'][0]['name']
        aggregator_api = data['aggregator'][0]['api']
    else:
        aggregator_model = next((model['name'] for model in data['reference_models'] if model.get('aggregator')), None)
        aggregator_api = next((model['api'] for model in data['reference_models'] if model.get('aggregator')), None)
    assert aggregator_model, f"Aggregator model not found"
    assert aggregator_api, f"Aggregator api not found"
    return aggregator_model, aggregator_api

