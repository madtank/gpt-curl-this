#!/usr/bin/env python3

import os
import sys
import subprocess
from getpass import getpass
import uuid

try:
    import sgpt
except ImportError:
    print("Please install shell-gpt first:")
    print("pip install shell-gpt")
    sys.exit(1)

def run_sgpt_command(session_id, prompt, code=False):
    options_list = ["--code --chat"] if code else ["--chat"]
    if session_id:
        options_list.append(session_id)
    command = ["sgpt"] + options_list + [f'"{prompt}"']
    command_str = " ".join(command)
    print("Running command:", command_str)
    result = subprocess.run(command_str, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def chat(session_id):
    print(f"Starting chat session: {session_id}")
    print("Enter your message or type 'exit' to return to the main menu.")
    while True:
        message = input("You: ").strip()
        if message.lower() == "exit":
            break

        try:
            prompt = f"{message}"
            print(f"Sending prompt to sgpt: {prompt}")
            result = run_sgpt_command(session_id, prompt, code=False)  # Removed options=[] from the function call
            if result:
                print("GPT-3:", result)
            else:
                print("No response generated. Please try again.")
        except Exception as e:
            print(f"Error occurred: {e}")
            should_continue = input("Session has reached its maximum capacity. Would you like to continue with a new session? (y/n): ").strip().lower()
            if should_continue == "y":
                session_id = str(uuid.uuid4())
                print(f"New session created: {session_id}")
            else:
                break


def code_interaction(session_id):
    print("Supported languages: Bash, PowerShell, Ruby, JavaScript, Python")
    print("Type 'exit' to return to the main menu.")
    print("")

    while True:
        language = input("Select language (Bash, PowerShell, Ruby, JavaScript, Python): ").strip().lower()

        if language == "exit":
            break

        if language not in ["bash", "powershell", "ruby", "javascript", "python"]:
            print("Invalid language selection. Please choose from Bash, PowerShell, Ruby, JavaScript, or Python.")
        else:
            print("Enter multiple queries separated by semicolons (;), or type 'exit' to return to language selection.")
            while True:
                query = input(f"{language.capitalize()} code: ").strip()
                if query.lower() == "exit":
                    break

                result = run_sgpt_command(session_id, query, code=True)

                if result is not None:
                    print("Generated code:")
                    print(result)
                else:
                    print("No code generated. Please try again.")
def main():
    os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY') or getpass("Please enter your OpenAI API key: ")

    print("Welcome to the enhanced Shell GPT!")
    print("Type 'exit' to quit the interactive mode.")
    print("")

    while True:
        mode = input("Select mode (Code, Chat): ").strip().lower()
        session_id = str(uuid.uuid4())
        if mode == "exit":
            break
        elif mode == "code":
            code_interaction(session_id)
        elif mode == "chat":
            chat(session_id)
        else:
            print("Invalid mode selection. Please choose from Code or Chat.")

if __name__ == "__main__":
    main()
