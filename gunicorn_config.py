import threading
import os

from gunicorn.arbiter import Arbiter

from test_turinga import ChatServer, AIHandler, UserHandler


def on_starting(server: Arbiter) -> None:
    chat_server = ChatServer(
        [AIHandler("./llama-2-13b-chat.Q5_K_M.gguf"), UserHandler()]
    )
    threading.Thread(
        target=chat_server.main,
        args=("0.0.0.0", int(os.environ.get("CHAT_PORT", 5000))),
        daemon=True,
    ).start()
    if server.log is not None:
        server.log.info("Chat server started.")
