import os

from flask import Blueprint, render_template


class FrontendServer(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__("frontend", __name__, *args, **kwargs)
        self.route("/", methods=["GET"])(self.home)
        self.chat_port = os.environ.get("CHAT_PORT", 5000)

    def home(self):
        return render_template("index.html", chat_port=self.chat_port)
