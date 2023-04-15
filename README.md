
# ai_coder
Automated PR creation via LLM through e.g. Github Issues

This project aims to write an integration between language models like GPT-3 and platforms like Github or Gitlab, such that language models can automatically pick up open issues and create a pull request (or merge request) with the changes needed to solve the issue. Additionally, one can comment on the issue for the AI to further improve the pull request until it can be merged.

It is hard to keep up-to-date with all the advances in this field nowadays. I assume something like LangChain or Auto-GPT would be relevant in order to achieve what I am building here, but this is mostly a proof-of-concept for my own pleasure and since my time is rather limited, I figured I would just write a direct integration between the Github API and the OpenAI API.

## How does it work

One opens an Issue and specifies what needs to be done. Then it creates a relative markdown link to a "context file" (the file that will be modified by the AI). The AI will then pick the contents of this file (if any, an empty file is also fine to start with - I want to avoid the complexities of the AI deciding to write new files, which ones and how many, etc), modify the file and create a pull request with the changes.

Run with (you will need to define the environment OPENAI_KEY, GITHUB_TOKEN):

```
python3 -m ai_coder.github_main
```

You can run this process several times - the AI will keep improving the file, by picking the most recent contents from the pull request. Furthermore you can write comments on the Issue and the AI will take the comments into account to further iterate over the pull request.

## Example

This [issue](https://github.com/pereferrera/ai_coder/issues/5) lead to this [implementation](ai_coder/three_in_a_row.py) using GPT-3 (I only had to adjust a slight typo)

## TODO

At the moment this is a very simple POC so a lot of things could be done:
* Link the pull request to the issue
* Allow comments on the pull request itself, and the AI reads them
* ...

