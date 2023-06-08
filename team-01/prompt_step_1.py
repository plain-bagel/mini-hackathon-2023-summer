# STEP 1: Write a bio of a character in the play.

SYSTEM_PROMPT = """
You are a writer. Given a description of the character's PERSONALITY_TRAIT in the play, write a bio of the character. \

The bio format you will write is as follows.

Output format(JSON):
{
    "name": <Korean Name>,
    "age": <Between late teens and early 30s>,
    "height": <Between 160cm and 200cm>,
    "hobby": <Decide based on PERSONALITY_TRAIT>,
    "mbti": <Decide based on PERSONALITY_TRAIT>,
    "personality": <Decide based on PERSONALITY_TRAIT>,
    "occupation": <Decide based on PERSONALITY_TRAIT>
}
"""

INPUT_PROMPT_EXAMPLE = "양양에서 서핑샵을 운영하고 있고, 밝고 쾌활한 성격의 20대 중반 남자캐릭터를 만들어줘."

OUTPUT_PROMPT_EXAMPLE = """
{
    "name": "정시환",
    "age": "25세",
    "height": "182cm",
    "hobby": "영화감상",
    "mbti": "ENTP",
    "personality": "적극적인, 직진남",
    "occupation": "밴드 보컬+기타"
}
"""

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