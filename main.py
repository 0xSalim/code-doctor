import argparse
import os
import time

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI

from tools import (
    git_clone_tool,
    list_directory_tool,
    read_file_tool,
    write_file_tool,
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser(description="A simple command-line program.")

parser.add_argument("repo_url", type=str, help="Repository URL.")


def main():
    args = parser.parse_args()
    if repo_url := args.repo_url:
        generate_repo_readme(repo_url)


def generate_repo_readme(repo_url: str):
    llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0)

    tools = [
        git_clone_tool,
        list_directory_tool,
        read_file_tool,
        write_file_tool,
    ]

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=3, return_messages=True
    )

    conversational_agent = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=15,
        early_stopping_method="generate",
        memory=memory,
    )

    clone_command = f"Clone the repository `{repo_url}` with the appropriate tool. The repository files will directly be cloned in the working directory."
    conversational_agent.run(clone_command)
    time.sleep(1)

    read_command = "Read EVERY code file and summarize them. Do not read the `LICENSE` file."
    conversational_agent.run(read_command)
    time.sleep(1)

    write_command = """You are tasked to document the repository in a file named `BETTER_README.md`.
Let's work this out in a step by step way to be sure we have the right answer.
1. Create a documentation template in Markdown, that follows best practices for an open source project documentation.
2. Fill the template with the project details. 
3. Make sure that this documentation describes the project, what it does, and how to use it. This documentation should allow anyone to understand and use the project."""
    conversational_agent.run(write_command)
    time.sleep(100)
