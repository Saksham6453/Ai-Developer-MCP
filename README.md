# ⚡ DevMCP — AI Developer Assistant

> An AI-powered developer assistant built with **Model Context Protocol (MCP)**, **FastMCP**, **Gemini**, and **Streamlit** for intelligent codebase exploration and Git analysis.

---

## 🚀 Overview

**DevMCP** is an AI Developer Assistant that allows developers to interact with a Python codebase using natural language.

Instead of manually searching through files, functions, classes, and Git history, the user can ask questions such as:

- "Where is the login function implemented?"
- "Explain the login flow."
- "Show me the project structure."
- "Find where authentication is used."
- "What changed recently in Git?"

The application uses an **MCP Server** to expose codebase and Git capabilities as tools. A custom **MCP Client** connects to the server, while **Gemini** acts as the reasoning layer that decides which tools to use.

---

## 🧠 Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Streamlit UI   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Agentic Layer   │
                    │ client/agent.py  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Gemini       │
                    │   LLM / Brain    │
                    └────────┬─────────┘
                             │
                     Tool Selection
                             │
                             ▼
                    ┌──────────────────┐
                    │   MCP Client     │
                    │  FastMCP Client  │
                    └────────┬─────────┘
                             │
                       STDIO Transport
                             │
                             ▼
                    ┌──────────────────┐
                    │   DevMCP Server  │
                    │     FastMCP      │
                    └────────┬─────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
        Codebase Tools   Git Tools      Workspace
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                    ┌──────────────────┐
                    │ Python Codebase  │
                    └──────────────────┘
Core components
Component	Responsibility
Streamlit	User interface
Gemini	LLM and tool-selection/reasoning layer
MCP Client	Connects to and invokes MCP server tools
MCP Server	Exposes developer capabilities through MCP
FastMCP	MCP server/client framework
Agentic Loop	Handles repeated tool calls and tool results
Workspace System	Restricts operations to the configured project
Git Tools	Provides Git status, diff and log information
🛠️ MCP Tools

DevMCP currently exposes the following MCP tools.

Codebase Tools
get_project_structure()

Returns the file structure of the configured workspace.

read_file(relative_path)

Reads a file from the configured workspace.

search_code(query)

Searches Python files for a given text query and returns matching files and line numbers.

find_function(function_name)

Uses Python's AST to locate functions across the codebase.

find_class(class_name)

Uses Python's AST to locate classes across the codebase.

Git Tools
git_status()

Returns the current Git working-tree status.

git_diff()

Returns the current Git diff.

git_log()

Returns the latest Git commits.

🤖 Agentic Tool Calling

One of the main goals of this project was to build an agentic MCP workflow rather than simply connecting an LLM to a single tool.

For example, when the user asks:

Explain how the login flow works.

Gemini can determine that it needs information from the codebase and request MCP tools.

A possible flow is:

Gemini
   │
   ├── read_file("app/main.py")
   │
   ├── read_file("app/auth.py")
   │
   └── read_file("app/users.py")
          │
          ▼
      MCP Server
          │
          ▼
      Tool Results
          │
          ▼
       Gemini
          │
          ▼
    Final Explanation

The agent continues calling tools until it has enough information to answer the user's question.

📁 Project Structure
AI Developer MCP/
│
├── server/
│   ├── __init__.py
│   ├── main.py
│   ├── mcp_server.py
│   ├── workspace.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── codebase.py
│       └── git.py
│
├── client/
│   ├── main.py
│   ├── agent.py
│   ├── llm.py
│   ├── gemini_adapter.py
│   └── tool_adapter.py
│
├── ui/
│   └── app.py
│
├── config/
│   └── workspace.json
│
├── tests/
│
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
└── .gitignore
🔍 How It Works
1. User asks a question

The question is entered through the Streamlit interface.

"Where is the login function implemented?"
2. Agent sends the request to Gemini

Gemini receives the available MCP tool definitions.

It determines that the find_function tool can answer the question.

3. Gemini requests an MCP tool
find_function(
    function_name="login"
)
4. MCP Client invokes the MCP Server

The custom MCP client sends the tool request to the DevMCP server using STDIO transport.

5. MCP Server executes the tool

The server searches the configured workspace using Python AST analysis.

Example result:

app/main.py
line: 5
function: login
arguments: username, email
6. Result is returned to Gemini

Gemini receives the tool result and generates a natural-language response.

7. Streamlit displays the result

The UI displays:

The final answer
MCP tools used
Tool arguments
Conversation history
🧩 Workspace Configuration

DevMCP operates on a configured local Python workspace.

The workspace is configured through:

config/workspace.json

Example:

{
    "workspace_path": "PATH_TO_YOUR_PROJECT"
}

Replace the path with the local project you want DevMCP to analyze.

The workspace helper resolves paths and prevents access outside the configured workspace.

🔐 Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

Never commit .env or your API key to GitHub.

The project should contain .env in .gitignore.

⚙️ Requirements
Python 3.11+
uv
Git
Gemini API key

Main technologies:

Python
FastMCP
MCP
Google GenAI SDK
Gemini
Streamlit
Git
Python AST
📦 Installation
1. Clone the repository
git clone <your-repository-url>
cd "AI Developer MCP"
2. Install dependencies

Using uv:

uv sync
3. Configure Gemini

Create:

.env

and add:

GEMINI_API_KEY=your_gemini_api_key
4. Configure the workspace

Edit:

config/workspace.json

and point it to the Python project you want DevMCP to analyze.

▶️ Running DevMCP

From the project root:

uv run streamlit run ui/app.py

If required on Windows, set the project root in PYTHONPATH:

$env:PYTHONPATH="."
uv run streamlit run ui/app.py

The Streamlit interface will open in your browser.

🧪 Example Queries

Once DevMCP is running, try:

Where is the login function implemented?
Explain the login flow across the project.
Find all places where authenticate is used.
Show me the project structure.
Find the get_user_by_username function.
Check the recent Git changes.
Show me the latest commits.
🎯 What I Learned From This Project

This project was built to understand MCP practically rather than only theoretically.

Key concepts implemented:

MCP architecture
MCP Server development
MCP Client development
STDIO transport
FastMCP
MCP tool registration
Tool discovery
Tool invocation
Tool schema conversion
Gemini function calling
Agentic tool-calling loops
Returning tool results to an LLM
Python AST-based code analysis
Git integration
Workspace isolation
Streamlit integration
📚 MCP Learning Journey

Before building DevMCP, I studied the core MCP concepts including:

Why MCP is needed
MCP architecture
MCP lifecycle
MCP server development
Local MCP servers
Remote MCP servers
MCP clients
Connecting clients and servers

I then built smaller MCP projects before using those concepts to create DevMCP.

🚧 Current Scope

DevMCP currently focuses on:

Codebase exploration
Python function/class discovery
Code search
File reading
Project structure analysis
Git inspection
AI-powered reasoning over tool results

It is intentionally kept as a focused learning and portfolio project rather than a full production IDE replacement.

🔮 Possible Future Improvements

Potential future extensions include:

Test execution through controlled MCP tools
Python syntax checking
Dependency analysis
Error/traceback analysis
More advanced code navigation
Workspace selection through the UI
Additional Git operations
Better tool-result visualization
Remote MCP deployment
👨‍💻 Author

Saksham Sharma

MCA — Artificial Intelligence & Machine Learning
