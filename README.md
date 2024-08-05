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
OpeaAI, Groq, DeepInfra, Together, Mistral, Nvidia, Deepseek, Hugging Face, Anthropic, Google Gemini, Cohere

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
    export COHERE_API_KEY={your_key}  <- web search
```
2. ### Install Requirements:
```
   conda create -n any_moa
   conda activate any_moa
   pip install pyaml, aiohttp, groq, together, openai, mistralai, huggingface_hub, anthropic, google-cloud-aiplatform, cohere
```

3. ### Run the interactive CLI script:
2 params: yaml file, number of layers<br>
`python bot.py  config\mixed_reference_models.yaml 3` 

#### Model file
Mixed model file contains models from different API vendors: Groq, Together, OpenAI, Mistra, Nvidia, DeepSeek, Hugging Face, Google Gemini, Deepinfra, and Cohere
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

## Configuration

The MOA system can be configured through modification/creation of new YAML files in 'config' dir:

## License

This project is licensed under the Apache 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Groq](https://groq.com/) for providing the underlying language models
- [Together AI](https://www.together.ai/) for proposing the Mixture of Agents architecture and providing the conceptual image

## Related Articles

Check out my [Medium article](https://medium.com/p/23f4fd43e72d) for more information about this project.

