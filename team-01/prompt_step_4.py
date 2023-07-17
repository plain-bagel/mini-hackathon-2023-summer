# mypy: ignore-errors
# Step 4: Generate a behind story of the character.

import prompt_step_1


SYSTEM_PROMPT = """
You are a writer. Using a bio of a character in the play, write more DETAILS about the character.

The DETAILS format you will write is as follows.

Output format(JSON):
{
    "happy_moment": <Write about the character's happy moment.>,
    "tragic_moment": <Write about the character's tragic moment.>,
    "current_life": <Write about the present of the character.>
}"""

INPUT_PROMPT_EXAMPLE = prompt_step_1.OUTPUT_PROMPT_EXAMPLE

OUTPUT_PROMPT_EXAMPLE = {
    "happy_moment": "정시환의 소중한 순간은 자신이 찍은 한 장의 사진이 매거진에 게재되었을 때입니다. 그 순간 그는 자신의 열정과 노력이 인정되는 것을 느꼈고, 자신의 작품이 많은 사람들에게 영감을 주는 역할을 하게 되었습니다. 이 순간은 그에게 자부심과 성취감을 안겨주었으며, 이후로 더욱 열심히 사진을 찍어 자신의 예술적인 면모를 발전시키고자 노력하고 있습니다.",
    "tragic_moment": "정시환의 비극적인 순간은 가족과의 갈등 때문에 가정 붕괴의 고통을 겪었던 시기입니다. 그는 가정 내부의 갈등과 이해 부족으로 인해 가족과의 소중한 인연을 잃게 되었고, 그로 인해 깊은 상처와 슬픔을 경험했습니다. 이 사건은 그에게 가족의 중요성과 소중함을 다시 깨닫게 하였으며, 이후로는 가족 간의 소통과 화합을 위해 노력하고 있습니다.",
    "current_life": "현재 정시환은 인플루언서로서 성공을 이루었고, 사진 작가로서도 자신만의 스타일과 명성을 얻고 있습니다. 그는 꾸준한 노력과 열정으로 자신의 창작 활동을 이어가며, 다양한 프로젝트와 협업을 통해 창의적인 작업을 선보이고 있습니다. 정시환은 사람들과의 만남을 즐기며 소통을 통해 새로운 영감을 얻고, 그들에게 자신의 작품과 이야기를 전달하는 것을 즐기고 있습니다. 그의 삶은 계속해서 성장하고 발전하며, 사진과 예술을 통해 자신의 의미 있는 이야기를 전달하는 데 주력하고 있습니다."
}


def get_messages(user_input: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": INPUT_PROMPT_EXAMPLE},
        {"role": "assistant", "content": str(OUTPUT_PROMPT_EXAMPLE)},
        {"role": "user", "content": user_input},
    ]
