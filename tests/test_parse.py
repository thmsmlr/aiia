import aiia.parse


def test_parse_messages():
    data = aiia.parse.parse_chat_markdown(
        """\
>>> Write me a haiku

🤖 GPT: 

Silent drifting clouds
Unfurl whispers on green slopes
Nature's soft secrets

>>> Thank you

🤖 GPT: 

You're welcome

    """
    )

    assert data["messages"] == [
        {"role": "user", "content": "Write me a haiku"},
        {
            "role": "assistant",
            "content": "Silent drifting clouds\nUnfurl whispers on green slopes\nNature's soft secrets",
        },
        {"role": "user", "content": "Thank you"},
        {"role": "assistant", "content": "You're welcome"},
    ]


def test_parse_frontmatter():
    data = aiia.parse.parse_chat_markdown(
        """\
---
title: test
model: gpt-4
---

>>> Write me a haiku

🤖 GPT: 

Silent drifting clouds
Unfurl whispers on green slopes
Nature's soft secrets

>>> Thank you

🤖 GPT: 

You're welcome

    """
    )

    assert data["metadata"] == {
        "title": "test",
        "model": "gpt-4",
    }
