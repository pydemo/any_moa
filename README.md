# any_moa
Mixture Of Agents with flexible input model sets from different API vendors.
Yet another fork from [grog-moa](https://github.com/skapadia3214/groq-moa?tab=readme-ov-file) and [together-moa](https://github.com/togethercomputer/MoA?tab=readme-ov-file#multi-layer-moa-example)

![MOA Architecture](https://github.com/togethercomputer/MoA/blob/main/assets/moa-3layer.png?raw=true)
*Source: Adaptation of [Together AI Blog - Mixture of Agents](https://www.together.ai/blog/together-moa)*


## Features

- Interactive chat interface
- Configurable model list/source and number of layers 
- Real-time streaming of responses



## CLI Demo

This CLI demo showcases a multi-layer inference API where the final response is aggregated from various reference models.

To run one shot or interactive demo, follow these 3 steps:

### Export Your API Keys:
```
    export TOGETHER_API_KEY={your_key}
    export GROQ_API_KEY={your_key}
    export DEEPINFRA_API_KEY={your_key}
```
### Install Requirements:
```
   conda create -n any_moa
   conda activate any_moa
   pip install pyaml, aiohttp, groq, together, groq
   
```
### Run the demo script:
 for Groq:  `python groq_moa.py`
 for Togeter:  `python together_moa.py`
 for DeepInfra `python deepinfra_moa.py`

### Run the interactive CLI script:
2 params: yaml file, number of layers<br>
`python bot.py  config\mixed_reference_models.yaml 3` 


#### Model file
Mixed model file contains models from different API vendors: Groq, Together, and Deepinfra
```
reference_models:
  - name: "llama3-70b-8192"
    api: "groq"
    aggregator: True
  - name: "Qwen/Qwen1.5-72B-Chat"
    api: "together"
  - name: "google/gemma-2-9b-it"
    api: "deepinfra"
  - name: "microsoft/WizardLM-2-7B"
    api: "deepinfra"
```
The CLI will prompt you to input instructions interactively:

1.  Begin by typing your prompt at the "Enter your prompt (Top things to do in Jersey City):" prompt.
2.  The system will process your input using predefined reference models.
3.  It will create a response based on the combined outputs from these models.
4.  You can keep the conversation going by entering additional prompts, with the system remembering the context of the ongoing interaction.

## Configuration

The MOA system can be configured through modification/creation of new YAML files in 'config' dir:

## Contributing

Contributions to this project are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with descriptive commit messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please ensure that your code adheres to the project's coding standards and includes appropriate tests and documentation.

## License

This project is licensed under the Apache 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Groq](https://groq.com/) for providing the underlying language models
- [Together AI](https://www.together.ai/) for proposing the Mixture of Agents architecture and providing the conceptual image

- 
