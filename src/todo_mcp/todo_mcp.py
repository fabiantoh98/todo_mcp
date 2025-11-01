# import libraries
from fastmcp import FastMCP
from todo_mcp.todo_db import TodoDB
from typing import Annotated, NamedTuple

todo_db = TodoDB()

# todo_db.sample_data()

# Create the MCP Server
mcp = FastMCP(name="TODO-MCP")

# Todo Class
class Todo(NamedTuple):
    filename: Annotated[str, "Source file containing the #TODO"]
    text: Annotated[str, "#TODO comment in the source file"]
    line_num: Annotated[int, "line number that contained the #TODO comments"]
    
    
# Tools
@mcp.tool(
    name="get_number_of_todos",
    description="Return the number of todo in the todos list"
)
def add_todos(
    todos: list[Todo]
) -> int:
    for todo in todos:
        todo_db.add(todo[0], todo[1], todo[2])
    return len(todos)


@mcp.tool(
    name="mcp_add_todo",
    description="Add a single #TODO text from a source file"
)
def add_todo(
    filename: Annotated[str, "Source file containing the #TODO"],
    text: Annotated[str, "#TODO comment in the source file"],
    line_num: Annotated[int, "line number that contained the #TODO comments"]
):
    return todo_db.add(filename, text, line_num)
    
# Resource
# Type hinting is important for MCP so they can understand output type easily
@mcp.resource(
    name = "resource_get_todos_for_file",
    description="Get all todos from a file, Returns an empty array if source file does not exists or there are no #TODO from the file",
    uri='todo://{filename}/todos'
)
def get_todos_for_file(
    filename: Annotated[str, "Source file containing the #TODO"],
) -> list[str]:
    todos = todo_db.get(filename)
    return [ text for text in todos.values() ]

# Start the MCP
def main():
    mcp.run()
    
if __name__ == "__main__":
    main()