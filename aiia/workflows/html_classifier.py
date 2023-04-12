# Because neovim is stupid and has broken indentation when there is nake left parens -.-
LEFT_PAREN = """
(
""".strip()
LEFT_BRACKET = """
[
""".strip()

PROMPT = """\
Answer the following questions as best you can. Can only use the following function call read the HTML document:

1. READ[part_number] 

    This function will read the HTML document part by part, it'll return the part of the document as defined by the page_number and the number of parts in the document.

2. ADD_TO_MEMORY[observation] 

    This function will allow you to save an observation to use later in your thinking sequence. 

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [READ, ADD_TO_MEMORY]
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
"""

import sys
import re
import aiia.gpt


def stream_response_until(prompt, stop_word="\nAction: "):
    response = ""
    for chunk in aiia.gpt.stream_response(
        # model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ):
        yield chunk

        response += chunk
        if stop_word in response:
            break


def run(question: str):
    memories = []
    print()
    print(f"Question: {question}")
    print()
    prompt = PROMPT.format(question=question)
    while True:
        print(prompt)
        print(memories)
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
                print(f"Final Answer: {clauses[-1][1]}")
                break

            if clauses[-2][0] != "Action":
                print("error", clauses)

            prompt = prompt.rsplit("\nObservation:", 1)[0]
            action = clauses[-2][1].strip()
            action_name = action.split(LEFT_BRACKET)[0]

            if action_name == "READ":
                page_number = int(action.split("READ[")[1].split("]")[0]) - 1
                CHUNK_SIZE = 2500
                result = open("/home/thomas/temp/index.html", "r").read()[
                    (CHUNK_SIZE * page_number) : (CHUNK_SIZE * (page_number + 1))
                ]
                observation = f"\nObservation: Result({page_number + 1} of 12)\n\n ```html\n{result}\n```\n"
                print(observation, end="")
                prompt += observation
            elif action_name == "ADD_TO_MEMORY":
                memories.append(action.split("ADD_TO_MEMORY[")[1].split("]")[0])
            else:
                print(f"Unknown action {action_name} text {action}")
                break

        else:
            print("No clauses found")


if __name__ == "__main__":
    run(
        """
        Find opening HTML tags for the container of an advertisement. Be sure to read the entire document before responding with the final answer.
    """.strip()
    )
