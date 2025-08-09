#!bin/bash

pip install -e .
pip install huggingface-hub
hf download TheBloke/Llama-2-13B-chat-GGUF llama-2-13b-chat.Q5_K_M.gguf