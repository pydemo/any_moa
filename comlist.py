import os
import cohere


api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)
response = co.models.list()
for model_d in response.models:
    print(model_d.name)
