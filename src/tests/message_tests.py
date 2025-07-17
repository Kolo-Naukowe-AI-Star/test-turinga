import unittest
import requests

class TestChatServer(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    def test_send_message_to_openai(self):
        payload = {
            "sender": "TestUser",
            "receiver": "ChatGPT",
            "text": "Hello, ChatGPT!"
        }
        response = requests.post(f"{self.BASE_URL}/send", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("OpenAI reply:", data.get("reply"))
        self.assertIn("reply", data)

    def test_get_messages(self):
        params = {
            "user1": "TestUser",
            "user2": "ChatGPT"
        }
        response = requests.get(f"{self.BASE_URL}/messages", params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Conversation:", data.get("messages"))
        self.assertIn("messages", data)

if __name__ == "__main__":
    unittest.main()