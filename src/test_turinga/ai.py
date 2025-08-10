from logging import getLogger
from typing import Sequence

from langchain_community.llms import LlamaCpp

logger = getLogger(__name__)


class Agent:
    """Agent class that utilizes LLM to respond to messages."""

    def __init__(self, prompt: str, llm: LlamaCpp):
        logger.debug("Agent __init__ called")
        self.prompt = prompt
        self.llm = llm

    def send_message(
        self, message: str, previous_messages: Sequence[str] | None = None
    ) -> str:
        prompt = (
            "[INST] <<SYS>>\n"
            f"{self.prompt.strip()}\n"
            "Previous messages: "
            f"{', '.join(previous_messages) if previous_messages else 'None'}"
            "<</SYS>>\n"
            f"{message.strip()} [/INST]"
        )
        logger.debug("Sending prompt to LLM:" + prompt)
        response = self.llm.invoke(prompt, max_tokens=64, stop=["[/INST]"])
        logger.debug(f"LLM response: {response!r}")
        if not response:
            logger.warning("No response received from LLM.")
        return response.strip().split("\n")[0] if response else "[No response]"


MASTER_PROMPT = (
    "Your name is {name}, you are a {age} year old. You are pretending to "
    "be a human. Do not under any circumstances reveal your true identity. You are "
    "communicating with a human through a chat. Messages coming from the human will "
    "be marked with the prefix 'User:'. Respond concisely and directly to the user's "
    "latest message in a single sentence. Do not include any additional context or "
    "dialogue."
)


# https://python.langchain.com/api_reference/community/llms/langchain_community.llms.llamacpp.LlamaCpp.html#llamacpp


class AgentFactory:

    def __init__(self, model_path: str):
        logger.debug("Loading LlamaCpp model...")
        self.llm = LlamaCpp(
            # for now set lower specs for better performance, need to test on better hardware
            model_path=model_path,
            n_gpu_layers=3,
            # n_batch=1024,
            n_batch=256,
            # n_ctx=4096,
            n_ctx=1024,
            f16_kv=False,
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            verbose=False,
        )
        logger.debug("LlamaCpp model loaded.")

    def new_agent(self, name: str, age: int) -> Agent:
        prompt = MASTER_PROMPT.format(name=name, age=age)
        logger.debug(f"Creating new agent with prompt:\n{prompt}\n")
        return Agent(prompt=prompt, llm=self.llm)
