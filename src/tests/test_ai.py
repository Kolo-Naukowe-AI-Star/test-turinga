import pytest
import os

from test_turinga.correspondents import AgentFactory


@pytest.fixture
def agent_factory():
    return AgentFactory(os.path.expanduser("~/llama-2-13b.Q4_0.gguf"))


def test_basic_response(agent_factory: AgentFactory):
    agent = agent_factory.new_agent("John", 20)
    response = agent.send_message("What is your name?")
    assert "John" in response
