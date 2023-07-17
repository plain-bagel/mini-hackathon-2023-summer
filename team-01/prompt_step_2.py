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

OUTPUT_PROMPT_EXAMPLE = {
    "appearance": "182cm에 탈색모로, 다양한 머리색을 즐기기 때문에 머릿결이 안 좋다. 탄탄하다기보단 낭창한 느낌의 체격. 전형적인 아이돌 상이지만 바른생활 인상과는 거리가 멀다. 어딘지 모르게 거친 느낌이 살짝 있어 모범적인 느낌은 아니다. ",
    "fashion": "밴드 보컬이자 연예인이라는 직업에 걸맞게 평소엔 펑크 장르의 룩을 자주 보여주지만 쉴 때는 오히려 단정하게 입는 편."
}


def get_messages(user_input: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": INPUT_PROMPT_EXAMPLE},
        {"role": "assistant", "content": str(OUTPUT_PROMPT_EXAMPLE)},
        {"role": "user", "content": user_input},
    ]
