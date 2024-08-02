# any_moa
Mixture Of Agents for with flexible input model sets from different API vendors.
Yet another fork from [grog-moa](https://github.com/skapadia3214/groq-moa?tab=readme-ov-file) and [tagether-moa](https://github.com/togethercomputer/MoA?tab=readme-ov-file#multi-layer-moa-example)

![MOA Architecture](https://github.com/togethercomputer/MoA/blob/main/assets/moa-3layer.png?raw=true)
*Source: Adaptation of [Together AI Blog - Mixture of Agents](https://www.together.ai/blog/together-moa)*


## Features

- Interactive chat interface powered by MOA
- Configurable main model and layer agents
- Real-time streaming of responses
- Visualization of intermediate layer outputs
- Customizable agent parameters through the UI

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/skapadia3214/groq-moa.git
   cd groq-moa
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

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

`python any_moa.py`

The CLI will prompt you to input instructions interactively:

1. Start by entering your instruction at the ">>>" prompt.
2. The system will process your input using the predefined reference models.
3. It will generate a response based on the aggregated outputs from these models.
4. You can continue the conversation by inputting more instructions, with the system maintaining the context of the multi-turn interaction.

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
