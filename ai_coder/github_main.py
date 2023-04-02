import regex as re
import os

import openai
from github import Github
from github.Issue import Issue
from github.Repository import Repository
from ai_coder.llms import prompt_gpt3

pattern = re.compile(r'\[([^][]+)\](\(((?:[^()]+|(?2))+)\))')


OPENAI_KEY_ENV = 'OPENAI_KEY'
GITHUB_KEY_ENV = 'GITHUB_TOKEN'

REQUIRED_ENV = [GITHUB_KEY_ENV,
                OPENAI_KEY_ENV]


def work_on(issue: Issue, repo: Repository):
    print(issue.body)

    for match in pattern.finditer(issue.body):
        description, _, url = match.groups()

        print(f"{description}: {url}")
        contents = repo.get_contents(url, ref='main')
        current_content = (
            contents.decoded_content.decode('utf-8')
        )

        target_branch = f'{issue.id}_ai_coder'

        # TODO not idempotent for now, would raise an Exception at some point
        # if run for a second time
        sb = repo.get_branch('main')
        repo.create_git_ref(ref=f'refs/heads/{target_branch}',
                            sha=sb.commit.sha)

        llm_question = ("""
You are an automated coding assistant and you just opened an Issue to work on.
The issue description is:

"{issue_description}"

The file that has to be modified has the following content:

"{file_contents}"

Please output the full content of the file which has to be modified,
after you applied the necessary modifications to tackle the issue at hand: 
""")
        modified_content = prompt_gpt3(llm_question.format(
            issue_description=issue.body,
            file_contents=current_content))

        repo.update_file(contents.path, "tackle issue",
                         modified_content, contents.sha, branch=target_branch)

        repo.create_pull(title=f"Tackle issue {issue.id}", body='',
                         head=target_branch, base="main")
        # TODO for now only one context file
        break


if __name__ == '__main__':
    if not all([env_key in os.environ for env_key in REQUIRED_ENV]):
        raise ValueError(f'Required environment variables: {REQUIRED_ENV}')

    g = Github(os.environ[GITHUB_KEY_ENV])
    openai.api_key = os.environ[OPENAI_KEY_ENV]

    repo = g.get_repo('pereferrera/ai_coder')

    for issue in repo.get_issues():
        if '[ai_coder]' in issue.title:
            # suitable for ai_coder
            work_on(issue, repo)
