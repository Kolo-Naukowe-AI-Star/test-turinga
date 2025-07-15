from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    text = data.get('text')
    if not sender or not receiver or not text:
        return jsonify({'error': 'Missing fields'}), 400
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
