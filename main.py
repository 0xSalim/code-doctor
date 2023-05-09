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
        max_iterations=3,
        early_stopping_method="generate",
        memory=memory,
    )

    question = f"""You need to enhance the README.md file in this repository: {repo_url}.
    Your task is the following:
    1. Clone the repository with the appropriate tool. The repository files will directly be cloned in the working directory.
    1. Read and understand what the repository does, by listing all files in `.`.
    2. Create a file named `BETTER_README.md`, that describes the project, what it does, and how to use it, in a Markdown format. This file should allow anyone to understand and use the project.
    Let's work this out in a step by step way to be sure we have the right answer."""

    print(question)
    conversational_agent.run(question)
    time.sleep(100)
