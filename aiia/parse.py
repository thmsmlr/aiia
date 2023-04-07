import re
import yaml


def parse_chat_markdown(contents):
    """Chat markdown is a markdown file with an optional yaml frontmatter"""
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
    """Convert a chat log to chat markdown"""
    yaml_frontmatter: str = yaml.safe_dump(chat["metadata"], sort_keys=False)
    markdown_body: str = ""

    for message in chat["messages"]:
        if message["role"] == "user":
            markdown_body += f">>> {message['content']}\n\n"
        elif message["role"] == "assistant":
            markdown_body += f"🤖 GPT:\n\n{message['content']}\n\n"

    return f"---\n{yaml_frontmatter}---\n\n{markdown_body}"
