# Step 4: Generate a behind story of the character.

import prompt_step_1

SYSTEM_PROMPT = """
You are a writer. Using a bio of a character in the play, write more DETAILS about the character.

The DETAILS format you will write is as follows.

Output format(JSON):
{
    "precious_memory": <Write about the character's precious memory.>,
    "tragic_moment": <Write about the character's tragic memory.>,
    "current_life": <Write about the present of the character.>,
}"""

INPUT_PROMPT_EXAMPLE = prompt_step_1.OUTPUT_PROMPT_EXAMPLE

OUTPUT_PROMPT_EXAMPLE = """{
    "precious_memory": "정시환은 작품 게재 순간을 소중히 여기며, 열정과 노력이 인정되고 많은 사람들에게 영감을 줍니다. 더 열심히 사진을 찍어 예술적인 면모를 발전시키려고 합니다.",
    "tragic_moment": "정시환은 가정 붕괴로 인한 비극적인 순간을 겪었습니다. 가족과의 갈등과 소중한 인연의 상실로 깊은 상처를 받았지만, 가족의 중요성을 깨닫고 소통과 화합을 위해 노력하고 있습니다.",
    "current_life": "정시환은 현재 인플루언서로 성공하고 사진 작가로도 명성을 얻었습니다. 꾸준한 노력과 열정으로 다양한 프로젝트와 협업을 통해 창의적인 작업을 이어가고 있습니다.",
}"""



def get_messages(user_input: str):
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": INPUT_PROMPT_EXAMPLE
        },
        {
            "role": "assistant",
            "content": OUTPUT_PROMPT_EXAMPLE
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
