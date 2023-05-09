import argparse
import os

from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI

from tools import clone_tool, list_directory_tool, read_file_tool

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser(description="A simple command-line program.")

parser.add_argument("repo_url", type=str, help="Repository URL.")


def main():
    args = parser.parse_args()
    if repo_url := args.repo_url:
        generate_repo_readme(repo_url)


def generate_repo_readme(repo_url: str):
    llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.2)

    tools = [clone_tool, list_directory_tool, read_file_tool]

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=3, return_messages=True
    )

    conversational_agent = initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method="generate",
        memory=memory,
    )

    question = f"""Generate a README file for this repository: {repo_url}. You need to clone it with the appropriate tool.
    Only output the README.md file content in a Markdown format and nothing else."""

    print(question)
    conversational_agent.run(question)
