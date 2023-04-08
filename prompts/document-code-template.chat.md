---
title: Untitled
model: gpt-4
prompt: |
  I am going to give you some code to rewrite.
  Only repond with a markdown codeblock of only the lines that changed.
---

>>> Consider the following function

```{language}
{selection}
```

Add or rewrite the function definition with types and a docstring. The docstring should include a description of the `:params:` and `:returns:`. 

Only repond with a markdown codeblock of only the lines that changed.
