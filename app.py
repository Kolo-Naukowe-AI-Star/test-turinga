import argparse
from flask import Flask

from test_turinga import TuringServer


if __name__ == "__main__":
    args = argparse.ArgumentParser("Turing Test Server")
    args.add_argument("--port", type=int, default=5000, help="Port to listen on")
    args.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    args.add_argument(
        "--debug", default=True, action="store_true", help="Enable debug mode"
    )
    args = args.parse_args()

    app = Flask(__name__)

    app.register_blueprint(TuringServer())

    app.run(host=args.host, port=args.port, debug=args.debug)
