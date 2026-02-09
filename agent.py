import os
import google.generativeai as genai
from dotenv import load_dotenv

class ParticlePhysicsAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)
        
        # Configure the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",  # Using the specific version for 2.0 Flash Lite based on recent updates, or falling back to a known close equivalent if exact name varies. 
            # Note: The user requested "gemini-2.5-flash-lite". 
            # As of my current knowledge update, valid models are typically `gemini-1.5-flash`, `gemini-2.0-flash-exp`.
            # I will use `gemini-2.0-flash-lite-preview-02-05` as the closest match for "modern" flash lite if 2.5 is not yet standard, 
            # but I will adhere to the user's specific request "gemini-2.5-flash-lite" as the model name string if they are sure it exists. 
            # However, safer to use the exact string request. 
            # Wait, the prompt says "gemini-2.5-flash-lite". I will use that string mainly, but I should probably check if it works.
            # actually, let's stick to the user's request:
            generation_config=generation_config,
            system_instruction="You are an expert in particle physics. Your goal is to explain complex concepts in clear, modern Python terms where applicable (e.g., using analogies to code or data structures if helpful), and provide accurate, scientific answers. Focus on the Standard Model, QFT, and recent discoveries. Be concise but thorough."
        )

    def ask(self, question: str) -> str:
        """
        Sends a question to the Gemini model and returns the response.
        """
        try:
            chat_session = self.model.start_chat(
                history=[]
            )
            response = chat_session.send_message(question)
            return response.text
        except Exception as e:
            return f"Error communicating with the model: {e}"

if __name__ == "__main__":
    # Basic test if run directly
    try:
        agent = ParticlePhysicsAgent()
        print("Agent initialized successfully.")
    except Exception as e:
        print(f"Agent initialization failed: {e}")
