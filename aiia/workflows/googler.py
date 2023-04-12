# Because neovim is stupid and has broken indentation when there is nake left parens -.-
LEFT_PAREN = """
(
""".strip()

PROMPT = """
Answer the following questions as best you can. You have access to the following tools:

1. `SEARCH(query) -> [webpage_links]` - This function searches the internet with a given query and returns a list of the top  webpage links that are related to the query.
2. `READ(webpage_link) -> webpage_content` - This function loads a webpage link and returns it's content

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [SEARCH, READ]
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
"""

import sys
import re
import asyncio
import aiia.gpt

from playwright.async_api import async_playwright
from readability import Document
from urllib.parse import urlencode


async def google_search(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()
        qs = urlencode({"q": query})
        await page.goto(f"https://www.google.com/search?{qs}")

        # Wait for search results to load
        await page.wait_for_load_state("networkidle")

        # Get the top 10 search result links
        search_results = await page.locator(".yuRUbf").all()
        top_links = []

        for result in search_results[:10]:
            link = result.locator("a").first
            url = await link.get_attribute("href")
            top_links.append(url)

        await browser.close()
        return top_links


async def read_webpage(url, max_words=250):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")

        # Get the main content using readability
        content = await page.content()
        document = Document(content)
        readable_content = document.summary()

        # Get the first 250 words
        text = re.sub("<[^<]+?>", "", readable_content)
        words = text.split()
        truncated_text = " ".join(words[:max_words]) + (
            "..." if len(words) > max_words else ""
        )

        await browser.close()
        return truncated_text


def stream_response_until(prompt, stop_word="\nAction: "):
    response = ""
    for chunk in aiia.gpt.stream_response(
        messages=[{"role": "user", "content": prompt}]
    ):
        yield chunk

        response += chunk
        if stop_word in response:
            break


def run(question: str):
    print()
    print(f"\033[34mQuestion:\033[0m {question}")
    print()
    print()
    prompt = PROMPT.format(question=question)
    while True:
        for chunk in stream_response_until(prompt, stop_word="\nObservation: "):
            prompt += chunk
            print(chunk, end="")
            sys.stdout.flush()

        print("\n", end="")

        clauses = re.findall(
            r"^([\w ]+):(.+?)(?:(?=\n\w+:)|$)", prompt, re.MULTILINE | re.DOTALL
        )
        if clauses:
            if clauses[-1][0] == "Final Answer":
                print()
                print()
                print(f"\033[34mFinal Answer:\033[0m")
                print(clauses[-1][1])
                break

            if clauses[-2][0] != "Action":
                print("error", clauses)

            prompt = prompt.rsplit("\nObservation:", 1)[0]
            action = clauses[-2][1].strip()
            action_name = action.split(LEFT_PAREN)[0]
            if action_name == "SEARCH":
                query = action.split("SEARCH(")[1].split(")")[0]
                result = asyncio.run(google_search(query))
                observation = f"\nObserveration: {result!r}\n"
                print(observation, end="")

                prompt += observation
            elif action_name == "READ":
                link = action.split("READ(")[1].split(")")[0]
                link = link.strip('"')
                link = link.strip("'")
                link = link.strip("`")
                result = asyncio.run(read_webpage(link))
                observation = f"\nObserveration: {result!r}\n"
                print(observation, end="")
                prompt += observation
            else:
                print(f"Unknown action {action}")
                break
        else:
            print("No clauses found")
            break

        print(prompt)


if __name__ == "__main__":
    run(
        """
        Get me a list of all the open source projects released by Stitch Fix
    """
    )
