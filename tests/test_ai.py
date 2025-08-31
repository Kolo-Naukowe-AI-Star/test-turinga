import pytest

from test_turinga.ai import AgentFactory

from .test_llama import MODEL_PATH


@pytest.fixture
def agent_factory():
    return AgentFactory(MODEL_PATH)


def test_new_agent(agent_factory):
    agent_factory.new_agent("John", 20)


def test_basic_response(agent_factory):
    agent = agent_factory.new_agent("John", 20)
    response = agent.send_message("What is your name?")
    assert "John" in response
