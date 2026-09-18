import json
from pathlib import Path

#connect to the file of dev project
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "workspace.json"

#LOad the configuration file
def get_workspace_path():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = json.load(file)

    workspace_path = Path(config["workspace_path"]).resolve()

    return workspace_path

def get_safe_path(relative_path):
    workspace = get_workspace_path()

    target = (workspace / relative_path).resolve()

    if not target.is_relative_to(workspace):
        raise ValueError("Access outside workspace is not allowed.")

    return target
if __name__ == "__main__":
    print(get_workspace_path())