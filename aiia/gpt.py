import os
import urllib.request
import urllib.parse
import json

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable required"


def get_response(messages, model="gpt-3.5-turbo"):
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
