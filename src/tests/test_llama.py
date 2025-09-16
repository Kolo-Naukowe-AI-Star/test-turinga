import os

import pytest
from langchain_community.llms import LlamaCpp

MODEL_PATH = os.path.realpath("./models/llama-2-13b-chat.Q5_K_M.gguf")


@pytest.fixture
def llm():
    return LlamaCpp(model_path=MODEL_PATH, n_ctx=1024, verbose=False)


def test_invoke(llm):
    message = "hi, what is your name?"
    prompt = (
        "[INST] <<SYS>>\n"
        "You are Alex, a helpful assistant. Only answer the user's latest message, concisely.\n"
        "<</SYS>>\n"
        f"{message} [/INST]"
    )
    response = llm.invoke(prompt, max_tokens=32, stop=["[/INST]"])
    assert "Alex" in response
