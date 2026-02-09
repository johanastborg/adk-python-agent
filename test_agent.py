import unittest
from unittest.mock import MagicMock, patch
from agent import ParticlePhysicsAgent

class TestParticlePhysicsAgent(unittest.TestCase):
    @patch('agent.genai')
    @patch('agent.os.getenv')
    def test_init(self, mock_getenv, mock_genai):
        # Mock API key presence
        mock_getenv.return_value = "fake_key"
        
        # Test initialization
        agent = ParticlePhysicsAgent()
        self.assertIsNotNone(agent.model)
        mock_genai.configure.assert_called_with(api_key="fake_key")

    @patch('agent.genai')
    @patch('agent.os.getenv')
    def test_ask(self, mock_getenv, mock_genai):
        mock_getenv.return_value = "fake_key"
        
        # Mock model response
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "The quark is a fundamental constituent of matter."
        
        mock_chat.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_chat
        
        mock_genai.GenerativeModel.return_value = mock_model

        agent = ParticlePhysicsAgent()
        response = agent.ask("What is a quark?")
        
        self.assertEqual(response, "The quark is a fundamental constituent of matter.")

if __name__ == '__main__':
    unittest.main()
