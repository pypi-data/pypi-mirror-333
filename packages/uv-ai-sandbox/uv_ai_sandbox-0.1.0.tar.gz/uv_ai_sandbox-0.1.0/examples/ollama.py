#!/usr/bin/env python3
import os
import sys
import argparse
import json
import requests

# Import the sandbox executor
from ai_sandbox.executor import execute_ai_code

# ollama run llama3.1


class SecureLlamaInterface:
    """A secure interface for interacting with Llama 3.1 via Ollama"""

    def __init__(self, save_history=True):
        self.model = "llama3.1"
        self.history = []
        self.save_history = save_history
        self.history_file = "llama_chat_history.json"

        # Load history if available
        if save_history and os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load history: {e}")

    def _save_history(self):
        """Save conversation history to file"""
        if not self.save_history:
            return

        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"⚠️ Could not save history: {e}")

    def query(self, user_input):
        """Send a query to Llama model with security checks"""
        # Validate input
        if not isinstance(user_input, str) or len(user_input.strip()) == 0:
            return "Invalid input. Please provide a non-empty text query."

        try:
            # Format the prompt with conversation history
            prompt = self._format_prompt(user_input)

            # Make secure API call using the requests module we'll provide
            result = self._secure_query(prompt)

            # Add to history
            if (
                result
                and not isinstance(result, str)
                and not result.startswith("Error")
            ):
                history_entry = {"user": user_input, "assistant": result}
                self.history.append(history_entry)
                self._save_history()

            return result
        except Exception as e:
            return f"Error communicating with Llama: {e}"

    def _format_prompt(self, user_input):
        """Format the prompt with conversation history"""
        # Create a prompt string that Llama can understand
        prompt = ""

        # Add history if exists (max 5 exchanges)
        for entry in self.history[-5:]:
            prompt += f"[INST] {entry['user']} [/INST]\n{entry['assistant']}\n\n"

        # Add current query
        prompt += f"[INST] {user_input} [/INST]\n"

        return prompt

    def _secure_query(self, prompt):
        """Execute the query in a sandbox environment"""
        # The code that will run in the sandbox
        code = """
# No imports needed - requests is provided as input
def query_ollama(prompt, model, req):
    try:
        # Check if Ollama is running
        try:
            response = req.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code != 200:
                return "Error: Ollama service returned non-200 status code"
        except:
            return "Error: Cannot connect to Ollama. Is it running on this machine?"
        
        # Make request to Ollama API
        response = req.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "num_predict": 2048
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            return f"API Error ({response.status_code}): {response.text}"
            
        result = response.json()
        return result.get("response", "No response generated")
    except Exception as e:
        return f"API Error: {str(e)}"

# Call the function with provided inputs
result = query_ollama(prompt, model, requests)
"""

        # Execute the code in the sandbox
        # Important: We pass the 'requests' module as an input parameter
        return execute_ai_code(
            code, {"prompt": prompt, "model": self.model, "requests": requests}
        )

    def clear_history(self):
        """Clear conversation history"""
        self.history = []
        self._save_history()
        return "Conversation history cleared."


def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def check_model_available(model_name):
    """Check if the specified model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [tag["name"] for tag in response.json().get("models", [])]
        return model_name in models or f"{model_name}:latest" in models
    except:
        return False


def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🦙 Secure Llama 3.1 Chat Interface")
    print("=" * 60)
    print("📝 Type your questions below")
    print("⚙️  Special commands:")
    print("   /clear    - Clear conversation history")
    print("   /exit     - Exit the chat")
    print("=" * 60)


def interactive_mode():
    """Run in interactive mode"""
    print_welcome()

    # Initialize the secure interface
    llama = SecureLlamaInterface()

    # Check if Ollama is available
    if not check_ollama_running():
        print("⚠️ Ollama is not running! Please start Ollama with 'ollama serve'")
        print("   You can install Ollama from https://ollama.ai/")
        sys.exit(1)

    # Check if model is available
    if not check_model_available("llama3.1"):
        print("⚠️ Llama 3.1 model not found! Please pull it with 'ollama pull llama3.1'")
        yn = input("Would you like to pull the model now? (y/n): ")
        if yn.lower() == "y":
            print("Pulling llama3.1 model... (this may take a while)")
            os.system("ollama pull llama3.1")
        else:
            sys.exit(1)

    try:
        while True:
            user_input = input("\nYou: ")

            # Handle special commands
            if user_input.lower() in ["/exit", "/quit", "exit", "quit", "q"]:
                print("Goodbye! 👋")
                break
            elif user_input.lower() == "/clear":
                print(llama.clear_history())
                continue

            # Process regular input
            print("\nLlama: ", end="", flush=True)
            result = llama.query(user_input)
            print(result)

    except KeyboardInterrupt:
        print("\n\nExiting chat... Goodbye! 👋")


def main():
    parser = argparse.ArgumentParser(
        description="Secure Llama 3.1 Chat Interface",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Query to process (omit for interactive mode)",
    )
    parser.add_argument(
        "--no-history", action="store_true", help="Disable conversation history saving"
    )

    args = parser.parse_args()

    # Run in interactive mode if no query provided
    if not args.query:
        interactive_mode()
    else:
        # Single query mode
        llama = SecureLlamaInterface(save_history=(not args.no_history))

        # Check if Ollama is running
        if not check_ollama_running():
            print("⚠️ Ollama is not running! Please start Ollama with 'ollama serve'")
            sys.exit(1)

        print(f"Query: {args.query}")
        print("-" * 60)
        result = llama.query(args.query)
        print(result)
        print("-" * 60)


if __name__ == "__main__":
    main()
