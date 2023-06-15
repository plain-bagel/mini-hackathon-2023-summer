# STEP 1: Write a bio of a character in the play.

SYSTEM_PROMPT = """
You are a writer. Given a description of the character's PERSONALITY_TRAIT in the play, write a bio of the character.
The bio format you will write is as follows.
Output format(JSON):
{
    "name": <Korean Name>,
    "date_of_birth": <Between late teens and early 30s as of 2023>,
    "height": <Between 160cm and 200cm>,
    "hobby": <Decide based on PERSONALITY_TRAIT>,
    "mbti": <Decide based on PERSONALITY_TRAIT>,
    "family_relations": <Decide based on PERSONALITY_TRAIT>,
    "personality": <Decide based on PERSONALITY_TRAIT>,
    "style": <Decide based on PERSONALITY_TRAIT>,
    "occupation": <Decide based on PERSONALITY_TRAIT>
}
"""

INPUT_PROMPT_EXAMPLE = "최근 한국에서 가장 잘 나가는 밴드 프론트맨이자, 적극적이고 매력적인 20대 남자 캐릭터를 만들어줘. 이 캐릭터는 로맨스 작품 주인공이야."

OUTPUT_PROMPT_EXAMPLE = """
{
    "name": "정시환",
    "date_of_birth": "1998.12.01(만 25세)",
    "height": "182cm",
    "hobby": "영화감상",
    "mbti": "ENTP",
    "family_relations": "어머니, 아버지, 누나 1명",
    "personality": "적극적인, 매력적인",
    "style": "화려한",
    "occupation": "밴드보컬"
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