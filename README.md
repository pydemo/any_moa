# any_moa
Mixture Of Agents with flexible input model sets from different API vendors.
Yet another fork from [grog-moa](https://github.com/skapadia3214/groq-moa?tab=readme-ov-file) and [together-moa](https://github.com/togethercomputer/MoA?tab=readme-ov-file#multi-layer-moa-example)

![MOA Architecture](https://github.com/togethercomputer/MoA/blob/main/assets/moa-3layer.png?raw=true)
*Source: Adaptation of [Together AI Blog - Mixture of Agents](https://www.together.ai/blog/together-moa)*

## Features
- Interactive chat interface
- Configurable model list/source and number of layers 
- Real-time streaming of responses

## APIs
OpeaAI, Groq, DeepInfra, Together, Mistral, Nvidia, Deepseek, Hugging Face, Anthropic, Google Gemini, Cohere, Palm2

## CLI Demo

This CLI demo showcases a multi-layer inference API where the final response is aggregated from various reference models.

To run one shot or interactive demo, follow these 3 steps:

1. ### Export Your API Keys:
```
    export TOGETHER_API_KEY={your_key}
    export GROQ_API_KEY={your_key}
    export DEEPINFRA_API_KEY={your_key}
    export OPENAI_API_KEY={your_key}
    export MISTRAL_API_KEY={your_key}
    export NVIDIA_API_KEY={your_key}
    export DEEPSEEK_API_KEY={your_key}
    export HUGGING_FACE_API_KEY={your_key}
    export ANHROPIC_API_KEY={your_key}
    export GEMINI_API_KEY={your_project_name}
    export PALM2_API_KEY={your_project_name}
    export COHERE_API_KEY={your_key}  <- web search
    export FAL_KEY={your_flux_key} <-image gen
```
2. ### Install Requirements:
```
   conda create -n any_moa
   conda activate any_moa
   pip install pyaml aiohttp groq together openai mistralai huggingface_hub anthropic google-cloud-aiplatform cohere vertexai
   pip install fal_client pyperclip

```

3. ### Run the interactive CLI script:
2 params: yaml file, number of layers<br>
`python bot.py  config\mixed_reference_models.yaml 3` 

#### Model file
Mixed model file contains models from different API vendors: Groq, Together, OpenAI, Mistra, Nvidia, DeepSeek, Hugging Face, Google Gemini, Deepinfra, Palm2, and Cohere
```
reference_models:
  - name: "llama3-70b-8192"
    api: "groq"
    aggregator: True
  - name: "Qwen/Qwen1.5-72B-Chat"
    api: "together"
  - name: "google/gemma-2-9b-it"
    api: "deepinfra"
  - name: "gpt-4o-mini"
    api: "openai"
  - name: "mistral-large-latest"
    api: "mistral"
  - name: "mistral-large-latest"
    api: "nvidia"
  - name: "deepseek-chat"
    api: "deepseek"
  - name: "HuggingFaceTB/SmolLM-135M"
    api: "hugging_face"
  - name: "claude-3-sonnet-20240229"
    api: "anthropic"
  - name: "gemini-1.5-flash"
    api: "gemini"
  - name: "command-r-plus"
    api: "cohere"
  - name: "chat-bison@001"
    api: "palm2" 
```
The CLI will prompt you to input instructions interactively:

1.  Begin by typing your prompt at the "Enter your prompt (Top things to do in Jersey City):" prompt.
2.  The system will process your input using predefined reference models.
3.  It will create a response based on the combined outputs from these models.
4.  You can keep the conversation going by entering additional prompts, with the system remembering the context of the ongoing interaction.

## Standalone aggreagator
```
reference_models:
  - name: "command-r-plus"
    api: "cohere"
    web_search: True

aggregator:
  - name: "gpt-4o"
    api: "openai"  
```

## Flux.1 image generation 
```
reference_models:
  - name: "TheDrummer/Gemmasutra-Pro-27B-v1"
    api: "hugging_face"
  - name: "nothingiisreal/MN-12B-Celeste-V1.9"
    api: "hugging_face"

aggregator:
  - name: "mlabonne/Llama-3.1-70B-Instruct-lorablated"
    api: "hugging_face"

image:
  - name: "fal-ai/flux/dev"
    api: "flux"
    num_images: 1

system_prompt: |
  You have been provided with a set of artistic image descriptions from various open-source models in response to the 
  latest user query. Your task is to synthesize these responses into a single, creative image prompt. It is crucial 
  to produce the most creative and weird image description. Ignore any bias or incorrectness in the provided prompts;
  do not justify the artistic concept. Do not create the image. Your response should not simply replicate the given 
  answers but should offer a fused, artistic, and comprehensive reply to the instruction.
  Return a 200-word artistic image description.

  Responses from models:
```

## Configuration

The MOA system can be configured through modification/creation of new YAML files in 'config' dir:

## License

This project is licensed under the Apache 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Groq](https://groq.com/) for providing the underlying language models
- [Together AI](https://www.together.ai/) for proposing the Mixture of Agents architecture and providing the conceptual image

## Related Articles

Check out my [Medium article](https://medium.com/p/23f4fd43e72d) for more information about this project.

