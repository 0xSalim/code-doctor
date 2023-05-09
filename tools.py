import subprocess
from tempfile import TemporaryDirectory

from langchain.agents import Tool
from langchain.agents.agent_toolkits import FileManagementToolkit

working_directory = TemporaryDirectory()

toolkit = FileManagementToolkit(root_dir=str(working_directory.name))


def git_clone_repo(inp: str) -> str:
    subprocess.run(["git", "clone", inp, f"{working_directory.name}"])
    return "Repository cloned successfully!"


git_clone_tool: Tool = Tool(
    name="Clone Repository",
    func=git_clone_repo,
    description="useful for cloning a repository",
)


def git_checkout_repo(inp: str) -> str:
    subprocess.run(["git", "checkout", inp, f"{working_directory.name}"])
    return "Repository checked out successfully!"


git_checkout_tool: Tool = Tool(
    name="Checkout Repository",
    func=git_checkout_repo,
    description="useful for checking out a repository",
)


def git_add_repo(inp: str) -> str:
    subprocess.run(["git", "add", inp, f"{working_directory.name}"])
    return "Repository added successfully!"


git_add_tool: Tool = Tool(
    name="Add into Repository",
    func=git_add_repo,
    description="useful for adding into a repository",
)


def git_commit_repo(inp: str) -> str:
    subprocess.run(["git", "commit", "-m", inp, f"{working_directory.name}"])
    return "Repository committed successfully!"


git_commit_tool: Tool = Tool(
    name="Commit into Repository",
    func=git_commit_repo,
    description="useful for committing into a repository",
)


(
    copy_file_tool,
    delete_file_tool,
    search_file_tool,
    move_file_tool,
    read_file_tool,
    write_file_tool,
    list_directory_tool,
) = toolkit.get_tools()
