import uuid
from typing import Callable

from flask import request, jsonify, Blueprint, Response, abort

from .thread import Thread
from .correspondents import User, AgentFactory

UID_HEADER = "X-User-ID"


def id_required(
    func: Callable[["TuringServer", User], Response]
) -> Callable[["TuringServer"], Response]:
    """Decorator to verify that the ID is registered, and retrieve the user."""

    def wrapper(self, *args, **kwargs):
        user_id = request.headers.get(UID_HEADER)
        if not user_id:
            abort(400)

        user = self.users.get(user_id)
        if not user:
            abort(403)

        return func(self, user, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# TODO add matchmaking, maybe once a user connects and there's an unassigned channel?


class TuringServer(Blueprint):

    def __init__(self, model_path: str | None = None, *args, **kwargs):
        super().__init__("turing_server", __name__, *args, **kwargs)
        self.channels: list[Thread] = []
        self.users: dict[str, User] = {}
        if model_path:
            self.agent_factory = AgentFactory(model_path)

        self.add_url_rule(
            "/messages", "send_message", self.message_received, methods=["POST"]
        )
        self.add_url_rule(
            "/messages", "get_messages", self.retrieve_messages, methods=["GET"]
        )
        self.add_url_rule("/handshake", "handshake", self.handshake, methods=["GET"])
        self.add_url_rule("/status", "status", self.retrieve_status, methods=["GET"])

    def find_channel(self, user: User) -> Thread | None:
        try:
            return next(c for c in self.channels if user in c)
        except StopIteration:
            return None

    def handshake(self):
        id = str(uuid.uuid4())
        self.users[id] = User(id)
        return jsonify(id=id)

    @id_required
    def message_received(self, user: User) -> Response:
        message = request.form.get("content")
        if not message:
            abort(400)

        channel = self.find_channel(user)
        if not channel:
            abort(400)

        channel.received_message(user, message)
        return jsonify()

    @id_required
    def retrieve_messages(self, user: User):
        return jsonify(messages=user.pop())

    @id_required
    def retrieve_status(self, user: User):
        return jsonify(ready=self.find_channel(user) is not None)
