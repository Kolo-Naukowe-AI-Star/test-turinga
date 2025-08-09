import argparse
import threading
from flask import Flask

from server import run_socket_server

if __name__ == "__main__":
    args = argparse.ArgumentParser("Turing Test Server")
    args.add_argument("--model_path", type=str, default="./llama-2-13b-chat.Q5_K_M.gguf", help="Path to the llm model")
    args.add_argument("--port", type=int, default=5000, help="Port to listen on")
    args.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    args.add_argument(
        "--debug", default=True, action="store_true", help="Enable debug mode"
    )
    args = args.parse_args()

    # Start socket server in a background thread
    socket_thread = threading.Thread(
        target=run_socket_server,
        args=(args.model_path, args.host, args.port),
        daemon=True
    )
    socket_thread.start()

    app = Flask(__name__)

    app.register_blueprint(TuringServer(args.model_path))

    app.run(host=args.host, port=args.port, debug=args.debug)
