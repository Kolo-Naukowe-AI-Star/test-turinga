#!/usr/bin/bash

python main.py --model_path "./models/Bielik-11B-v2.3-Instruct.Q8_0.gguf" --host "$(dig +short $(hostname) | head -n 1)" --port "$1"
