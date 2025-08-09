# test-turinga

## Setup

run setup.sh in bash to install all needed dependencies / llm

```bash
python server.py # to start up server (right now it has 50/50 chance for matching with AI / waiting for another user)
python client.py # to join as user
```

## Tests

```bash
pip install -e .[dev]
pytest
```

## LLM

The LLM is stored on
[Hugging Face](https://huggingface.co/), specifically [here](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/blob/main/llama-2-13b-chat.Q5_K_M.gguf)
you can always use the [download_llm.sh](./download_llm.sh) script to
download it.
