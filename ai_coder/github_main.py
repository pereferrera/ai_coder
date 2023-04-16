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
    if issue.closed_at:
        print('Ignoring closed issue')
        return

    print(f' -- Working on: "{issue.body}"')

    for match in pattern.finditer(issue.body):
        description, _, url = match.groups()

        print(f" > Found context file to work on: {description}: {url}")

        comment_context = ''
        pr_id = None

        for comment in issue.get_comments():
            if '[ai_coder]' not in comment.body:
                comment_context += f"\n- {comment.body}\n"
            else:
                if ' Opening PR ' in comment.body:
                    pr_id = int(comment.body[
                        (comment.body.index(' Opening PR ')
                         + len(' Opening PR ')):].rstrip())
                    print(f'We are already working on this on PR #{pr_id}')

        target_branch = f'{issue.id}_ai_coder'

        try:
            sb = repo.get_branch('main')
            repo.create_git_ref(ref=f'refs/heads/{target_branch}',
                                sha=sb.commit.sha)

            contents = repo.get_contents(url, ref='main')
        except Exception as e:
            print(f'{e} - Branch probably exists already')
            contents = repo.get_contents(url,
                                         ref=f'refs/heads/{target_branch}')

        current_content = (
            contents.decoded_content.decode('utf-8')
        )
        llm_question = ("""
You are an automated coding assistant and you just opened an Issue to work on.
The issue description is:

"{issue_description}"

The file to work on has the following content:

{file_contents}
""")

        if comment_context:
            llm_question += ("""

Additionally, the following comments have been made to you after you have
already started working on this issue:

{comment_context}
""").format(comment_context=comment_context)

        llm_question += ("""
Please output the full content of the file which has to be modified,
after you applied the necessary modifications to tackle the issue at hand:
""")

        llm_question = llm_question.format(issue_description=issue.body,
                                           file_contents=current_content)
        print(llm_question)

        modified_content = prompt_gpt3(llm_question)

        if modified_content != current_content:
            repo.update_file(contents.path, "tackle issue",
                             modified_content, contents.sha,
                             branch=target_branch)

            if pr_id is None:
                try:
                    pr = repo.create_pull(
                        title=f"Tackle issue {issue.id}", body='',
                        head=target_branch, base="main")

                    issue.create_comment(f'[ai_coder] Opening PR {pr.number}')
                except Exception as e:
                    raise Exception(
                        f'{e} - Pull request probably exists? but pr_id '
                        'is None!')
            else:
                pr = repo.get_pull(pr_id)

            issue.create_comment(f'Worked on it: {pr.html_url}')
        else:
            print('LLM does not want to perform any new change for now.')

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
