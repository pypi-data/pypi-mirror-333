## Python Environment Setup
We recommend using pyenv to manage your Python environments and to use Python 3.9.11. For example:

```bash
pyenv install 3.9.11
pyenv virtualenv 3.9.11 copilot_env
pyenv activate copilot_env
```

## Installing Dependencies
Once your environment is active, install the required dependencies:

```bash
# Install the local package with extras from tecton-gen-ai root
pip install -e ".[tecton,openai,dev]"
# Install other dependencies (pin lancedb to avoid arrow issue, and include logfire)
pip install \
    streamlit-flow-component \
    black \
    lancedb==0.18.0 \
    logfire \
    streamlit \
    plotly \
    snowflake-connector-python \
    snowflake \
    matplotlib
```

## Tecton Login
Before starting the co-pilot, make sure you’re logged into your Tecton cluster:
```bash
    tecton login yourcluster.tecton.ai
```

## Environment Variables
Set the following environment variables for Tecton and OpenAI:
```bash
export TECTON_API_KEY=<api key to the dev-gen-ai cluster>
export OPENAI_API_KEY=<api key to openai>
```

## Running the Co-Pilot
To start the co-pilot, run:

```bash
streamlit run --server.port 3000 demo/copilot/ui.py
```
