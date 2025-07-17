from .base import Correspondent

from langchain_community.llms import LlamaCpp


class Agent(Correspondent):
    """Agent class that utilizes LLM to respond to messages."""

    def __init__(self, prompt: str, llm: LlamaCpp):
        self.prompt = prompt
        self.llm = llm

    def send_message(self, message: str) -> str:
        input = f"Prompt:{self.prompt.strip()}\nUser:{message.strip()}"
        response = self.llm(input)
        return response


MASTER_PROMPT = """"Your name is %s, you are a %d year old. You are pretending to
be a human. Do not under any circumstances reveal your true identity. You are
communicating with a human through a chat. Messages coming from the human will
be marked with the prefix 'User:'. Respond concisely and directly to the user's
latest message in a single sentence. Do not include any additional context or
dialogue."""


# https://python.langchain.com/api_reference/community/llms/langchain_community.llms.llamacpp.LlamaCpp.html#llamacpp


class AgentFactory:

    def __init__(self, model_path: str):
        self.llm = LlamaCpp(
            model_path=model_path,
            # technical
            n_gpu_layers=3,  # how good your gpu is
            n_batch=1024,  # how many tokens to process at once
            n_ctx=8128,  # size of the context window
            f16_kv=False,  # half precision floats
            # prompt settings
            temperature=0.7,  # Lower temperature for more deterministic responses
            top_p=0.9,  # Adjust top-p sampling for more focused outputs
            top_k=40,  # Limit top-k sampling for less randomness
            # shutup
            verbose=False,
        )

    def new_agent(self, name: str, age: int) -> Agent:
        prompt = MASTER_PROMPT % (name, age)
        return Agent(prompt, self.llm)
