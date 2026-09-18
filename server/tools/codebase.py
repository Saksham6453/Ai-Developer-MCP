from pathlib import Path
import ast
from server.workspace import get_workspace_path, get_safe_path


# Project Structure
def get_project_structure():
    workspace = get_workspace_path()

    files = []

    for path in workspace.rglob("*"):
        if path.is_file():
            files.append(path.relative_to(workspace))

    return files

#Funtion to read a file
def read_file(relative_path):
    file_path = get_safe_path(relative_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {relative_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {relative_path}")

    return file_path.read_text(encoding="utf-8")

#Search file
def search_code(query):
    workspace = get_workspace_path()

    results = []

    for path in workspace.rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            if query.lower() in line.lower():
                results.append({
                    "file": str(path.relative_to(workspace)),
                    "line": line_number,
                    "content": line.strip()
                })

    return results

#Find function
def find_function(function_name):
    workspace = get_workspace_path()

    results = []

    for path in workspace.rglob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (UnicodeDecodeError, SyntaxError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == function_name:
                    results.append({
                        "file": str(path.relative_to(workspace)),
                        "line": node.lineno,
                        "name": node.name,
                        "arguments": [
                            arg.arg for arg in node.args.args
                        ]
                    })

    return results

#Find class
def find_class(class_name):
    workspace = get_workspace_path()

    results = []

    for path in workspace.rglob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (UnicodeDecodeError, SyntaxError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if node.name == class_name:
                    results.append({
                        "file": str(path.relative_to(workspace)),
                        "line": node.lineno,
                        "name": node.name
                    })

    return results

if __name__ == "__main__":
    structure = get_project_structure()

    for path in structure:
        print(path)