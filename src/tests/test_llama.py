import unittest
import os

from langchain_community.llms import LlamaCpp

MODEL_PATH = os.path.realpath("./llama-2-13b-chat.Q5_K_M.gguf")


class TestLlama(unittest.TestCase):
    def setUp(self):
        self.llm = LlamaCpp(model_path=MODEL_PATH, n_ctx=1024, verbose=False)

    def test_invoke(self):
        message = "hi, what is your name?"
        prompt = (
            "[INST] <<SYS>>\n"
            "You are Alex, a helpful assistant. Only answer the user's latest message, concisely.\n"
            "<</SYS>>\n"
            f"{message} [/INST]"
        )
        response = self.llm.invoke(prompt, max_tokens=32, stop=["[/INST]"])
        self.assertIn("Alex", response)
