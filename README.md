# test-turinga

Turing test showcase for the "Noc Naukowców 2025" event. Not actually at all
how a Turing test is conducted, but the core idea of checking if a machine can
pass as human is there.

## Setup

Run `setup.sh` in bash to install all needed dependencies / llm

```bash
./runserver.sh
./runclient.sh
```

## Tests

```bash
pytest -v src/tests/
```

## LLM

The LLM is stored on
[Hugging Face](https://huggingface.co/), you can always use the
[download_llm.sh](./download_llm.sh) script to download it.
