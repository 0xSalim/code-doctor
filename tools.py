import subprocess
from tempfile import TemporaryDirectory

from langchain.agents import Tool
from langchain.tools.file_management import ListDirectoryTool, ReadFileTool

working_directory = TemporaryDirectory()


def clone_repo(inp: str) -> str:
    subprocess.run(["git", "clone", inp, working_directory.name])
    return "Repository cloned successfully!"


clone_tool = Tool(
    name="Clone Repository",
    func=clone_repo,
    description="useful for cloning a repository",
)

read_file_tool = ReadFileTool()

list_directory_tool = ListDirectoryTool()
