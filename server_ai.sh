#!/bin/bash
CHAT_PORT=5000
export CHAT_PORT=$CHAT_PORT
gunicorn -w 4 -b :8080 app:app -c gunicorn_config.py
