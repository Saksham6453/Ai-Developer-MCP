from server.mcp_server import mcp
from server.tools.codebase import (
    get_project_structure,
    read_file,
    search_code,
    find_function,
    find_class,
)
from server.tools.git import (
    git_status,
    git_diff,
    git_log,
)

mcp.tool(get_project_structure)
mcp.tool(read_file)
mcp.tool(search_code)
mcp.tool(find_function)
mcp.tool(find_class)
mcp.tool(git_status)
mcp.tool(git_diff)
mcp.tool(git_log)

if __name__ == "__main__":
    mcp.run()