import re
import yaml

from typing import Dict, List, Union


def parse_chat_markdown(
    contents: str,
) -> Dict[str, Union[Dict[str, str], List[Dict[str, str]]]]:
    """This function parses the contents of a chat markdown file, which can include an optional
    YAML frontmatter, into a dictionary containing metadata and a list of messages. The messages
    are extracted in the format of role and content, where the role can be 'system', 'user', or
    'assistant'. The chat markdown file should have a specific structure, where user messages
    start with '>>>', assistant messages start with '🤖 GPT:', and optional YAML frontmatter
    is enclosed between '---' lines.

    Args:
        contents (str): The contents of the chat markdown file, with optional YAML frontmatter.

    Returns:
        dict: A dictionary containing two keys:
            - metadata (dict): The parsed YAML frontmatter, if present. Otherwise, an empty
            dictionary.  - messages (list): A list of dictionaries, each containing the 'role'
            (system, user, or assistant) and 'content' of the message.
    """
    pattern = re.compile(r"^---$", re.MULTILINE)
    matches = pattern.findall(contents)
    if len(matches) >= 2:
        parts = contents.split("---", 2)
        yaml_frontmatter = parts[1].strip()
        yaml_data = yaml.safe_load(yaml_frontmatter)
        markdown_body = parts[2].strip()
    else:
        yaml_data = {}
        markdown_body = contents.strip()

    messages = []
    message = ""
    role = ""

    if yaml_data.get("prompt"):
        messages.append({"role": "system", "content": yaml_data["prompt"]})

    for line in markdown_body.splitlines():
        if line.startswith(">>>"):
            if message:
                message = message.strip()
                messages.append(
                    {
                        "role": role,
                        "content": message,
                    }
                )
            role = "user"
            message = line[3:].strip() + "\n"
        elif line.startswith("🤖 GPT:"):
            if message:
                message = message.strip()
                messages.append(
                    {
                        "role": role,
                        "content": message,
                    }
                )
            role = "assistant"
            message = line[7:].strip() + "\n"
        else:
            message += line + "\n"

    if message:
        message = message.strip()
        messages.append(
            {
                "role": role,
                "content": message,
            }
        )

    return {
        "metadata": yaml_data,
        "messages": messages,
    }


def to_chat_markdown(chat: dict) -> str:
    """Converts chat messages to a formatted markdown string with YAML frontmatter.

    Args:
        chat (dict): A dictionary with the following structure:

    Returns:
        str: Formatted markdown string with YAML frontmatter
    """
    yaml_frontmatter: str = yaml.safe_dump(chat["metadata"], sort_keys=False)
    markdown_body: str = ""

    for message in chat["messages"]:
        if message["role"] == "user":
            markdown_body += f">>> {message['content']}\n\n"
        elif message["role"] == "assistant":
            markdown_body += f"🤖 GPT:\n\n{message['content']}\n\n"

    return f"---\n{yaml_frontmatter}---\n\n{markdown_body}"
