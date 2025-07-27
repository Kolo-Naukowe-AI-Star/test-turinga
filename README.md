# test-turinga

## Setup

```bash
pip install -e .
python3 app.py
```

## Tests

```bash
pip install -e .[dev]
pytest
```

## LLM

The LLM is stored on
[Hugging Face](https://huggingface.co/), specifically [here](https://huggingface.co/TheBloke/Llama-2-13B-GGUF/)
you can always use the [download_llm.sh](./download_llm.sh) script to
download it.
