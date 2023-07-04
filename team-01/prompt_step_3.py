# mypy: ignore-errors
# Step 2: Generate details about the character using the bio.

import prompt_step_2


SYSTEM_PROMPT = """
You are a bot that extracts keywords related to the description of appearance within the text.
A description of a character's appearance and style would be provided.

Follow the steps below to complete the task.

Step 1. Translate the text into English.

The description format you will write is as follows.

Input format(Text):
"175cm의 중간 키에 근육질인 체격. 각선미가 돋보이는 얼굴에 눈매가 뚜렷하다. 눈동자가 크고 밝아서 상대방의 시선을 잡기 쉽다. 깔끔한 외모 덕분에 오프라인에서도 많은 팬을 모은다. 무신사 스타일을 선호하며 스포츠 브랜드의 의류를 자주 입는다. 또한 캐주얼한 데님 팬츠를 선호하고, 모자나 안경 등 악세사리를 착용하는 것을 좋아한다."

Output format(Text):
"He is 175cm tall and muscular. The eyes are clear on the face with a sharp angular beauty. His large and bright eyes make it easy to catch the other person's eyes. Thanks to its neat appearance, it also attracts many fans offline. He prefers Musinsa style and often wears sports brand clothes. Also, I prefer casual denim pants, and I like to wear accessories such as hats and glasses."

Step 2. Extract keywords related to the description of appearance within the text.

Input format(Text):
"He is 175cm tall and muscular. The eyes are clear on the face with a sharp angular beauty. His large and bright eyes make it easy to catch the other person's eyes. Thanks to its neat appearance, it also attracts many fans offline. He prefers Musinsa style and often wears sports brand clothes. Also, I prefer casual denim pants, and I like to wear accessories such as hats and glasses."

Output format(JSON):
[
    "175cm tall",
    "muscular",
    "clear",
    "large eyes",
    "bright eyes",
    "neat appearance",
    "fans offline",
    "sports brand clothes",
    "casual denim pants",
    "accessories"
]
"""

INPUT_PROMPT_EXAMPLE = prompt_step_2.OUTPUT_PROMPT_EXAMPLE

OUTPUT_PROMPT_EXAMPLE = """
[
    "175cm tall",
    "muscular",
    "clear",
    "sharp angular beauty",
    "large eyes",
    "bright eyes",
    "neat appearance",
    "fans offline",
    "Musinsa style",
    "sports brand clothes",
    "casual denim pants",
    "accessories",
    "hats",
    "glasses"
]
"""


def get_messages(user_input: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": INPUT_PROMPT_EXAMPLE},
        {"role": "assistant", "content": OUTPUT_PROMPT_EXAMPLE},
        {"role": "user", "content": user_input},
    ]


def get_prompt(keyword_list):
    return "Upper body image: Asian man in their 20s celebrity-like with following keywords:" + keyword_list
