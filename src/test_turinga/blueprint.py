from openai import OpenAI
from flask import request, jsonify, Blueprint


# messages are sent via POST request to /send endpoint
# receive sent messages via GET request /messages


class TuringServer(Blueprint):

    def __init__(self, openai_client: OpenAI, *args, **kwargs):
        super().__init__("turing_server", __name__, *args, **kwargs)
        self.openai_client = openai_client
        self.messages = []

        self.add_url_rule(
            "/send", "send_message", self.message_received, methods=["POST"]
        )
        self.add_url_rule(
            "/messages", "get_messages", self.retrieve_messages, methods=["GET"]
        )

    def message_received(self):
        data = request.get_json()
        sender = data.get("sender")
        receiver = data.get("receiver")
        text = data.get("text")
        if not sender or not receiver or not text:
            return jsonify({"error": "Missing fields"}), 400

        if receiver.lower() == "chatgpt":
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}]
            )
            reply = response.choices[0].message.content
            self.messages.append({"sender": sender, "receiver": receiver, "text": text})
            self.messages.append(
                {"sender": receiver, "receiver": sender, "text": reply}
            )
            return jsonify({"status": "Message sent", "reply": reply})
        else:
            self.messages.append({"sender": sender, "receiver": receiver, "text": text})
            return jsonify({"status": "Message sent"})

    def retrieve_messages(self):
        user1 = request.args.get("user1")
        user2 = request.args.get("user2")
        if not user1 or not user2:
            return jsonify({"error": "Missing users"}), 400
        convo = [
            m
            for m in self.messages
            if (m["sender"] == user1 and m["receiver"] == user2)
            or (m["sender"] == user2 and m["receiver"] == user1)
        ]
        return jsonify({"messages": convo})
