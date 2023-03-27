#!/usr/bin/env python3

import os
import openai
import subprocess
from datetime import datetime
import readline

readline.parse_and_bind('"\e[A": history-search-backward')
readline.parse_and_bind('"\e[B": history-search-forward')

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

def chat_with_gpt(model, message):
    response = openai.ChatCompletion.create(
        model=model,
        messages=message
    )
    return response['choices'][0]['message']['content']

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
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

def main():
    # Initialize conversation with a system message
    conversation = [
        {"role": "system", "content": "You are a helpful assistant that can fetch local files or access web resources using file: and curl: commands."}
    ]

    max_tokens = 3000

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        if user_input.startswith("file:") or user_input.startswith("curl:"):
            request_type = "file" if user_input.startswith("file:") else "curl"
            resource = user_input[5:]

            approval = input(f"Would you like to fetch the content of '{resource}'? [y/n]: ")

            if approval.lower() == "y":
                try:
                    if request_type == "file":
                        content = read_file(resource)
                    else:
                        content = make_curl_command(resource)

                    trimmed_content = trim_content(content, max_tokens)
                    if content != trimmed_content:
                        print("Content has been trimmed due to token limit.")

                    conversation.append({"role": "user", "content": trimmed_content})
                    assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
                    print("Assistant:", assistant_response)
                    conversation.append({"role": "assistant", "content": assistant_response})

                    # Placeholder for handling remaining chunks
                    remaining_chunks = content[len(trimmed_content):]
                    while len(remaining_chunks) > 0:
                        # Prompt the user for confirmation to process the remaining chunks
                        continue_processing = input("There are additional chunks to be processed. Do you want to continue? [y/n]: ")
                        if continue_processing.lower() == "y":
                            next_chunk = trim_content(remaining_chunks, max_tokens)
                            conversation.append({"role": "user", "content": next_chunk})
                            assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
                            print("Assistant:", assistant_response)
                            conversation.append({"role": "assistant", "content": assistant_response})
                            remaining_chunks = remaining_chunks[len(next_chunk):]
                        else:
                            break

                except (FileNotFoundError, Exception) as e:
                    print(f"Error while fetching {request_type} resource:", str(e))
            else:
                print("Resource request denied.")
        else:
            conversation.append({"role": "user", "content": user_input})
            assistant_response = chat_with_gpt("gpt-3.5-turbo", conversation)
            print("Assistant:", assistant_response)
            conversation.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    main()
