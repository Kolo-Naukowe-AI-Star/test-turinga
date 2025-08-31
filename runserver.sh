#!/usr/bin/bash

python -m test_turinga.main --model_path "./models/llama-2-13b-chat.Q5_K_M.gguf" --host "0.0.0.0" --port "5000"
