# mypy: ignore-errors
# Step 2: Generate details about the character using the bio.

import prompt_step_1


SYSTEM_PROMPT = """
You are a writer. Using a bio of a character in the play, write more details about the character.

The description format you will write is as follows.

Output format(JSON):
{
    "appearance": <Describe based on BIO>,
    "fashion": <Describe based on BIO>,
}"""

INPUT_PROMPT_EXAMPLE = prompt_step_1.OUTPUT_PROMPT_EXAMPLE

OUTPUT_PROMPT_EXAMPLE = """{
    "appearance": "탈색 헤어스타일에 약간 마른 체격. 전형적인 아이돌 느낌의 얼굴이다. 거친 느낌이 살짝 있다. 반항적인 느낌이다.",
    "fashion": "밴드 보컬이자 연예인이라는 직업에 걸맞게 평소엔 펑크 장르의 룩을 자주 보여준다. 쉴 때는 오히려 단정하게 입는 편."
}"""


def get_messages(user_input: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": INPUT_PROMPT_EXAMPLE},
        {"role": "assistant", "content": OUTPUT_PROMPT_EXAMPLE},
        {"role": "user", "content": user_input},
    ]
