# test-turinga

TODO: Update

## Setup

Run `setup.sh` in bash to install all needed dependencies / llm

```bash
./runserver.sh
./runclient.sh
```

## Tests

```bash
pytest -v tests/
```

## LLM

The LLM is stored on
[Hugging Face](https://huggingface.co/), specifically [here](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/blob/main/llama-2-13b-chat.Q5_K_M.gguf)
you can always use the [download_llm.sh](./download_llm.sh) script to
download it.
