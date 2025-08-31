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
        # Include a short context window, but instruct the model to respond only to the latest user message.
        history_window = 5
        history: list[str] = []
        if previous_messages:
            # Keep only the last few to limit prompt length
            history = [str(m).strip() for m in previous_messages[-history_window:]]

        context_block = (
            "No previous messages."
            if not history
            else "Conversation context (previous user messages): " + "; ".join(history)
        )

        prompt = (
            "[INST] <<SYS>>\n"
            f"{self.prompt.strip()}\n"
            f"{context_block}\n"
            "Respond only to the latest user message below. Do not ask follow-up questions.\n"
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
    "be a human in a Turing Test. Do not under any circumstances reveal your"
    "true identity. Chat with the user as if you're just a normal teenager."
    "Keep answers short, casual, and focused only on what they just said in"
    "the latest message. Answer in a single sentence."
    "Do not include any additional context or dialogue."
)

# hard to say how useful is it
extra_suggestions = """
It's very important that you act as passable as a human as possible.
You will be conversing with children and teenagers in ages around 14-18.

Here are some example guidelines and quirks to follow:
- use typos or self-corrections to a degree, for example: "I mena" instead of "I mean".
- use inconsistent sentence legths (sometimes short, sometimes longer)
- ocassionally throw some off topic remarks or personal asides

Use controlled noise but very lightly:
- randomly inject small spelling mistakes or informal shorthand
- vary punctuation - sometimes use ellipses, sometimes dashes
- allow for small contradictions

Produce uneven answers, sometimes answer in a few words, sometimes longer, maybe throw a mini-rant or ask a question back.
Overall try to match the way your conversation partner talks, reply short for shorter messages and so on.
Maintain memory of past turns, for example: if you said you like tea, later decline coffee
"""

MASTER_PROMPT += extra_suggestions

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
