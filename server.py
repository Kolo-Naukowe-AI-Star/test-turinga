from test_turinga import Server
import logging


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Turing Test Socket Server")
    parser.add_argument(
        "--model_path",
        type=str,
        default="./llama-2-13b-chat.Q5_K_M.gguf",
        help="Path to the LLM model",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--log_level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="[%(asctime)s %(levelname)s | %(thread)d:%(module)s:%(lineno)d]: %(message)s",
    )

    server = Server(args.model_path)
    server.main(args.host, args.port)
