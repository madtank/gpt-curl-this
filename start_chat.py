#!/usr/bin/env python3

import os
import openai
import subprocess
from datetime import datetime
import readline
import argparse

readline.parse_and_bind('"\e[A": history-search-backward')
readline.parse_and_bind('"\e[B": history-search-forward')
remaining_chunks = None

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

def chat_with_gpt(model, message):
    response = openai.ChatCompletion.create(
        model=model,
        messages=message
    )
    return response['choices'][0]['message']['content']

def read_file(file_path, message):
    with open(file_path, "r") as file:
        content = file.read()
    if message:
        content += "\n" + message
    return content

def make_curl_command(url, method="GET"):
    command = f"curl -X {method} {url}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Error executing curl command: {result.stderr}")
    return result.stdout

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_token_count(text, max_tokens):
    token_count = len(text.split())
    return token_count < max_tokens

def trim_content(text, max_tokens):
    tokens = text.split()
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = ' '.join(tokens)
        text += " [Content trimmed due to token limit]"
    return text

# Test cases
def run_single_test(command, question):
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can fetch local files or access web resources using file and curl commands. However, you cannot directly access the user's local files. Instead, you can guide the user on how to fetch the files locally and then provide their contents to you for processing."
        }
    ]

    print(f"Command: {command}")
    if command.startswith("file:"):
        file_name = command[5:].strip()
        assistant_response = f"I cannot directly access files on your local machine, as I am an AI running on a remote server. However, you can read the file '{file_name}' on your machine and provide its contents to me. Then, I can help you with any questions or tasks related to that content."
    elif command.startswith("curl"):
        url = command[5:].strip()
        assistant_response = f"I cannot directly access web resources using the curl command. Instead, you can fetch the web resource '{url}' on your machine and provide its contents to me. Then, I can help you with any questions or tasks related to that content."
    else:
        assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
    
    print("\033[1;33mAssistant:\033[0m", assistant_response)
    conversation.append({"role": "assistant", "content": assistant_response})

    print(f"Question: {question}")
    conversation.append({"role": "user", "content": question})
    assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
    print("\033[1;33mAssistant:\033[0m", assistant_response)
    conversation.append({"role": "assistant", "content": assistant_response})

def main():
    # Initialize conversation with a system message
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can fetch local files or access web resources using file: and curl commands. However, you cannot directly access the user's local files. Instead, you can guide the user on how to fetch the files locally and then provide their contents to you for processing."
        }
    ]

    if "TEST_COMMAND" in os.environ and "TEST_QUESTION" in os.environ:
        user_input = os.environ["TEST_COMMAND"]
        question = os.environ["TEST_QUESTION"]

    while True:
        user_input = input("\033[1;34mUser:\033[0m ")
        if user_input.lower().strip() == "exit":
            break

        if user_input.startswith("file:") or user_input.startswith("curl"):
            request_type = "file:" if user_input.startswith("file:") else "curl"
            resource_and_message = user_input[5:].split('"', 1)
            resource = resource_and_message[0].strip()
            message = resource_and_message[1].strip()[:-1] if len(resource_and_message) > 1 else ""

            approval = input(f"Would you like to fetch the content of '{resource}'? [y/n]: ")

            if approval.lower() == "y":
                try:
                    if request_type == "file:":
                        # Fetch the file content
                        content = read_file(resource, message)
                        print('message sent to assistant', content)
                        # Include context in the message
                        user_input = f"This is the content of the file: '{resource}' you have just accessed using your capabilities:\n\n{content}"
                    else:
                        # Fetch the content using curl
                        content = make_curl_command(resource)
                        # Include context in the message
                        user_input = f"This is the content you have just fetched using a curl command to '{resource}':\n\n{content}"
                        print('message sent to assistant', user_input)

                    # Send the message to the assistant
                    conversation.append({"role": "user", "content": user_input})
                    assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
                    print("\033[1;33mAssistant:\033[0m", assistant_response)
                    conversation.append({"role": "assistant", "content": assistant_response})

                    # Placeholder: handle remaining_chunks here (e.g., enhance the application to request additional chunks)
                    if remaining_chunks:
                        print("There are additional chunks to be processed.")
                except (FileNotFoundError, Exception) as e:
                    print(f"Error while fetching {request_type} resource:", str(e))
            else:
                print("Resource request denied.")
        else:
            conversation.append({"role": "user", "content": user_input})
            assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
            print("\033[1;33mAssistant:\033[0m", assistant_response)
            conversation.append({"role": "assistant", "content": assistant_response})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with Abby, your helpful assistant.")
    parser.add_argument('-t', '--test', action='store_true', help="Run test cases")
    args = parser.parse_args()

    if args.test:
        run_test_cases()
    else:
        main()