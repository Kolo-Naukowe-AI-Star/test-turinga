import argparse
from test_turinga import ChatServer, AIHandler, UserHandler, MessageHandler
import logging


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Turing Test Socket Server")
    parser.add_argument(
        "--model_path",
        type=str,
        help="Path to the LLM model",
    )
    parser.add_argument(
        "--no_user", action="store_true", help="Disable user connections"
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--log_level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="[%(asctime)s %(levelname)s | %(module)s:%(lineno)d]: %(message)s",
    )

    handlers: list[MessageHandler] = []
    if not args.no_user:
        handlers.append(UserHandler())
    if args.model_path:
        handlers.append(AIHandler(args.model_path))

    server = ChatServer(handlers)
    server.main(args.host, args.port)
