
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

def run_sgpt_command(prompt, code, options):
    options_list = ["--code"] if code else []
    result = subprocess.run(["sgpt"] + options_list + options + [prompt], capture_output=True, text=True)
    return result.stdout.strip()

def chat(session_id):
    print("Enter your message or type 'exit' to return to the main menu.")
    options = []
    while True:
        message = input("You: ").strip()
        if message.lower() == "exit":
            break

        try:
            result = run_sgpt_command(f"Chat session ID: {session_id}\n{message}", code=False, options=options)
            print(session_id)
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


def code_interaction():
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

                result = run_sgpt_command(query, code=True)

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

        if mode == "exit":
            break
        elif mode == "code":
            code_interaction()
        elif mode == "chat":
            session_id = str(uuid.uuid4())
            chat(session_id)
        else:
            print("Invalid mode selection. Please choose from Code or Chat.")

if __name__ == "__main__":
    main()
