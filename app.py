import os
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# messages are sent via POST request to /send endpoint
# receive sent messages via GET request /messages

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    text = data.get('text')
    if not sender or not receiver or not text:
        return jsonify({'error': 'Missing fields'}), 400

    if receiver.lower() == "chatgpt":
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        reply = response.choices[0].message.content
        messages.append({'sender': sender, 'receiver': receiver, 'text': text})
        messages.append({'sender': receiver, 'receiver': sender, 'text': reply})
        return jsonify({'status': 'Message sent', 'reply': reply})
    else:
        messages.append({'sender': sender, 'receiver': receiver, 'text': text})
        return jsonify({'status': 'Message sent'})

@app.route('/messages', methods=['GET'])
def get_messages():
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')
    if not user1 or not user2:
        return jsonify({'error': 'Missing users'}), 400
    convo = [m for m in messages if (m['sender'] == user1 and m['receiver'] == user2) or (m['sender'] == user2 and m['receiver'] == user1)]
    return jsonify({'messages': convo})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
