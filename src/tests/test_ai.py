import unittest

from test_turinga.ai import AgentFactory

from .test_llama import MODEL_PATH


class TestAgentFactory(unittest.TestCase):
    def setUp(self):
        self.agent_factory = AgentFactory(MODEL_PATH)

    def test_new_agent(self):
        self.agent_factory.new_agent("John", 20)

    def test_basic_response(self):
        agent = self.agent_factory.new_agent("John", 20)
        response = agent.send_message("What is your name?")
        assert "John" in response
