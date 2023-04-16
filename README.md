
# ai_coder
Automated PR creation via LLM through e.g. Github Issues

This project aims to write an integration between language models like GPT-3 and platforms like Github or Gitlab, such that language models can automatically pick up open issues and create a pull request (or merge request) with the changes needed to solve the issue. Additionally, one can comment on the issue for the AI to further improve the pull request until it can be merged.

## Disclaimer

It is hard to keep up-to-date with all the advances in this field nowadays. I assume something like [LangChain](https://python.langchain.com/en/latest/index.html) or [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) would be relevant in order to achieve what I am building here, but this is mostly a proof-of-concept for my own pleasure and since my time is rather limited, I figured I would just write a direct integration between the Github API and the OpenAI API.

## How does it work

One opens an Issue prefixed by "[ai_coder]" in the title and specifies what needs to be done. Then it creates a relative markdown link to a "context file" (the file that will be modified by the AI). The AI will then pick the contents of this file (if any, an empty file is also fine to start with - I want to avoid the complexities of the AI deciding to write new files, which ones and how many, etc), modify the file and create a pull request with the changes.

Run with (you will need to install dependencies from `requirements.txt` and define the environment OPENAI_KEY, GITHUB_TOKEN):

```
python3 -m ai_coder.github_main
```

You can run this process several times - the AI will keep improving the file, by picking the most recent contents from the pull request. Furthermore you can write comments on the Issue and the AI will take the comments into account to further iterate over the pull request. It is theoretically possible that the AI does not want to perform any further change. In this case, the output of the program will contain the line "LLM does not want to perform any new change for now.".

## Example

See this [issue](https://github.com/pereferrera/ai_coder/issues/7) for an example on how the communication / process works.

## TODO (easier)

At the moment this is a very simple POC so a lot of things could be done:
* Allow comments on the pull request itself, and the AI reads them. Right now only comments on the Issue are allowed.
* Allow proper code reviews e.g. place comments on the code with the content of an inline review.
* Allow multiple steps (right now the AI can only work on one context file).

## TODO (future)

* Allow the AI to decide which files to change/create and/or write an integration with Auto-GPT.