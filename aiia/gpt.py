import os
import urllib.request
import urllib.parse
import json

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable required"

from typing import Any, Dict, Iterator, List


def stream_response(
    messages: List[Dict[str, Any]], model: str = "gpt-3.5-turbo"
) -> Iterator[str]:
    """
    Stream response from the OpenAI API for chat-based language models.

    :param messages: A list of message dictionaries with 'role' and 'content' keys.
    :param model: The name of the language model to use. Defaults to "gpt-3.5-turbo".
    :returns: An iterator yielding the content of the response.
    """
    payload = {"stream": True, "model": model, "messages": messages}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    url = "https://api.openai.com/v1/chat/completions"

    req = urllib.request.Request(url, json.dumps(payload).encode("utf-8"), headers)
    response = urllib.request.urlopen(req)

    for line in response:
        line = line.decode("utf-8")
        line = line.lstrip("data: ").strip()
        if not line:
            continue

        if line == "[DONE]":
            break

        data = json.loads(line)
        if data["object"] == "chat.completion.chunk":
            delta = data["choices"][0]["delta"]
            if delta != "":
                yield delta.get("content", "")


def get_response(*args, **kwargs) -> str:
    return "".join(stream_response(*args, **kwargs))
