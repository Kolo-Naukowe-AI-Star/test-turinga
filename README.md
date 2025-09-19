# test-turinga

Turing test showcase for the "Noc Naukowców 2025" event. Not actually at all
how a Turing test is conducted, but the core idea of checking if a machine can
pass as human is there.

## Setup

### Server

Run `setup.sh` in bash to install all needed dependencies / llm. Then running:

```bash
./runserver.sh 5000
```

should start the server on port 5000.

#### Cuda

On WMI cluster you will need to activate the conda env:

```bash
conda activate pytorch-gpu
```

before running the `setup.sh` script, to ensure that everything installs
correctly. On arch:

```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --no-cache-dir --force-reinstall
```

### Client

Here install the lib:

```bash
pip install -e .
```

This way you will avoid installing the dependencies for self hosting the LLM.
If you have already ran the `setup.sh` script, you can skip this step.
Then run the client:

```bash
python client_tk.py
```

## Tests

```bash
pytest -v src/tests/
```

## LLM

The LLM is stored on
[Hugging Face](https://huggingface.co/), you can always use the
[download_llm.sh](./download_llm.sh) script to download it.
