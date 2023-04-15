import openai


def prompt_gpt3(gpt_prompt: str) -> str:
    """returns the textual answer of GPT-3 (davinci 003) to the passed
    prompt"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=gpt_prompt,
        temperature=0.7,
        max_tokens=2048,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response['choices'][0]['text']
