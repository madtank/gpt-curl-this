#!/usr/bin/env python3

# Test cases are not sending file or doing curl commands at this time.

import os
from termcolor import colored
from start_chat import run_single_test

def run_test_cases():
    test_cases = [
        {
            "command": "file:color.txt",
            "question": "What is the color of the car according to color.txt file?"
        },
        {
            "command": "curl:https://raw.githubusercontent.com/madtank/code/master/jokes/README.md",
            "question": "In the README file you fetched, what type of database is used with the jokes application?"
        },
        {
            "command": "curl:https://jsonplaceholder.typicode.com/todos/1",
            "question": "What is the title of the first todo item?"
        }
    ]

    for idx, test_case in enumerate(test_cases, 1):
        print(colored(f"Running test case {idx}...", "green"))
        run_single_test(test_case['command'], test_case['question'])

if __name__ == "__main__":
    run_test_cases()
