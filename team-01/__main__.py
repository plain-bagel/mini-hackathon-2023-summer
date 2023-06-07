import json
import os
import dotenv
import streamlit as st
import openai
import pandas as pd

import multiprocessing as mp


# Load Environment variables and have them as constants
dotenv.load_dotenv()

# Get key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat(messages, stream=False, queue=None):
    """
    Generate text using ChatGPT as a separate process
    """
    try:
        gpt_res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=1000,
            stream=stream,
            messages=messages,
        )
    except Exception as e:
        print(e)
        if queue is not None:
            queue.put(None)
        return None

    # Add to queue (for inter-process communication)
    if queue is not None:
        if not stream:
            queue.put(gpt_res['choices'][0]['message'])
        else:
            # Add chunks to queue when streaming
            for chunk in gpt_res:
                try:
                    queue.put(chunk['choices'][0]['delta'])
                except EOFError:
                    continue
    return gpt_res



system_prompt = """
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
    "occupation": <Decide based on PERSONALITY_TRAIT>,
}
"""

example_input_prompt = "양양에서 서핑샵을 운영하고 있고, 밝고 쾌활한 성격의 20대 중반 남자캐릭터를 만들어줘."

example_output_prompt = """
{
    "name": "정시환",
    "age": "25세",
    "height": "182cm",
    "hobby": "영화감상",
    "mbti": "ENTP",
    "personality": "적극적인, 직진남",
    "occupation": "밴드 보컬+기타",
}
"""


def get_messages(user_input: str):
    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": example_input_prompt
        },
        {
            "role": "assistant",
            "content": example_output_prompt
        },
        {
            "role": "user",
            "content": user_input
        }
    ]


def set_up_default_view():
    st.title('가상 캐스팅')
    user_input = st.text_input('캐릭터의 성격을 알려주세요.', "유튜버 겸 모델 출신 인플루언서 SNS없이 못 사는 인생은 폼생폼사 20대 초반 남자 캐릭터 만들어 줘.")
    show_actor_profile(user_input)

def show_actor_profile(user_input: str):
    messages = get_messages(user_input)
    manager = mp.Manager()
    queue = manager.Queue()
    p = mp.Process(target=chat, args=(messages, True, queue))
    p.start()
    response = ""
    profile_rows = []
    while True:
        try:
            chunk = queue.get(timeout=3)
            if chunk == {}:
                break
            if 'content' in chunk:
                response += chunk['content']
                # print(response)
        except Exception as e:
            continue
    p.join(timeout=30)

    try:
        actor_profile_json = json.loads(response)
        profile = {
            "이름": actor_profile_json["name"], 
            "나이": actor_profile_json["age"], 
            "키": actor_profile_json["height"], 
            "취미": actor_profile_json["hobby"], 
            "MBTI": actor_profile_json["mbti"], 
            "성격": actor_profile_json["personality"], 
            "직업": actor_profile_json["occupation"]
        }
        df = pd.DataFrame([
            profile,
        ])
        st.table(df)
    except Exception as e:
        print(e)
        return



if __name__ == '__main__':
    set_up_default_view()

