#!/usr/bin/env python3
"""Update GIGACHAT_TOKEN in .env file."""
import pathlib
import sys

# Add ai directory to path to import modules
project_root = pathlib.Path(__file__).parent.parent
ai_dir = project_root / "ai"
sys.path.insert(0, str(ai_dir))

from utils import init_env
from gigachat import get_access_token

def update_token_in_env():
    """Fetch new token and update .env file."""
    project_root = pathlib.Path(__file__).parent.parent
    env_path = project_root / ".env"
    
    # Load environment variables
    init_env()
    token = get_access_token()
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        return 1
    
    # Read existing .env
    lines = env_path.read_text(encoding="utf-8").splitlines()
    
    # Update or add GIGACHAT_TOKEN
    key = "GIGACHAT_TOKEN"
    found = False
    new_lines = []
    
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={token}")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"{key}={token}")
    
    # Write back
    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"✓ Token updated in {env_path}")
    return 0

if __name__ == "__main__":
    sys.exit(update_token_in_env())

