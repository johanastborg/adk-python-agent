import unittest
from unittest.mock import MagicMock, patch
from agent import ParticlePhysicsAgent

class TestParticlePhysicsAgent(unittest.TestCase):
    @patch('agent.Agent')
    @patch('agent.Runner')
    @patch('agent.InMemorySessionService')
    @patch('agent.os.getenv')
    def test_init(self, mock_getenv, mock_session_service, mock_runner, mock_agent):
        # Mock API key presence
        mock_getenv.return_value = "fake_key"
        
        # Test initialization
        agent = ParticlePhysicsAgent()
        
        # Verify Agent was initialized
        mock_agent.assert_called()
        
        # Verify Runner was initialized
        mock_runner.assert_called()
        _, kwargs = mock_runner.call_args
        self.assertEqual(kwargs['app_name'], "particle_physics_app")
        # Ensure session service was passed
        self.assertIn('session_service', kwargs)

    @patch('agent.Agent')
    @patch('agent.Runner')
    @patch('agent.InMemorySessionService')
    @patch('agent.os.getenv')
    def test_ask(self, mock_getenv, mock_session_service, mock_runner, mock_agent):
        mock_getenv.return_value = "fake_key"
        
        # Mock runner response event
        mock_event = MagicMock()
        mock_part = MagicMock()
        mock_part.text = "The quark is a fundamental constituent of matter."
        
        # Structure: event.content.parts[0].text
        mock_event.content.parts = [mock_part]
        
        mock_runner_instance = mock_runner.return_value
        # Mock run to yield one event
        mock_runner_instance.run.return_value = [mock_event]

        agent = ParticlePhysicsAgent()
        response = agent.ask("What is a quark?")
        
        # Verify response extraction
        self.assertEqual(response, "The quark is a fundamental constituent of matter.")

if __name__ == '__main__':
    unittest.main()
