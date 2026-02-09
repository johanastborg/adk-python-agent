import os
import uuid

from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

class ParticlePhysicsAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        # Configure the model using ADK structure
        self.agent = Agent(
            model="gemini-2.5-flash-lite", 
            name="particle_physics_agent",
            description="Expert in particle physics, Standard Model, and QFT.",
            instruction="""You are an expert in particle physics. Your goal is to explain complex concepts in clear, modern Python terms where applicable (e.g., using analogies to code or data structures if helpful), and provide accurate, scientific answers. Focus on the Standard Model, QFT, and recent discoveries. Be concise but thorough."""
        )
        
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name="particle_physics_app",
            session_service=self.session_service,
            auto_create_session=True
        )
        
        # Simple session management for CLI usage
        self.user_id = "user_default"
        self.session_id = str(uuid.uuid4())

    def ask(self, question: str) -> str:
        """
        Sends a question to the agent using the ADK runner.
        """
        try:
            # Construct content object
            content = types.Content(parts=[types.Part(text=question)])
            
            responses = []
            # Run the agent
            for event in self.runner.run(
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=content
            ):
                # Collect text from model responses
                # We need to inspect event structure. 
                # Assuming event.content is present for model responses
                if hasattr(event, 'content') and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            responses.append(part.text)
            
            return "".join(responses).strip()
            
        except Exception as e:
            return f"Error communicating with ADK agent: {e}"
