import os
import sys
from agent import ParticlePhysicsAgent
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found. Please check your .env file.")
        print("Copy .env.example to .env and add your API key.")
        sys.exit(1)

    try:
        agent = ParticlePhysicsAgent()
        print("Welcome to the Particle Physics Agent!")
        print("Ask me anything about the Standard Model, QFT, or recent discoveries.")
        print("Type 'exit' or 'quit' to end the session.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            
            if not user_input:
                continue

            print("Agent: Thinking...", end="\r")
            response = agent.ask(user_input)
            print(f"Agent: {response}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
