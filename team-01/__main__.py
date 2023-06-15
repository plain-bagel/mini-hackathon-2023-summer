import json
import os
import dotenv
import streamlit as st
import openai
import pandas as pd

import multiprocessing as mp
import prompt_step_1
import prompt_step_2

# Load Environment variables and have them as constants
dotenv.load_dotenv()

# Get key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

def send_chat(messages, stream=False, queue=None):
    """
    Generate text using ChatGPT as a separate process
    """
    try:
        gpt_res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=1000,
            stream=stream,
            n=1,
            messages=messages,
        )
    except Exception as e:
        print(e)
        return None

    return gpt_res['choices'][0]['message']['content']



@st.cache_data()
def show_actor_profile(user_input):
    '''
    Step 1: Generate a bio of a character in the play.
    '''
    messages = prompt_step_1.get_messages(user_input)
    response = send_chat(messages)
    try:
        print("Step 1 response")
        print(response)
        actor_profile_json = json.loads(response)
        current_profile = {
            "name": actor_profile_json["name"], 
            "date_of_birth": actor_profile_json["date_of_birth"], 
            "height": actor_profile_json["height"], 
            "hobby": actor_profile_json["hobby"], 
            "mbti": actor_profile_json["mbti"], 
            "family_relations": actor_profile_json["family_relations"], 
            "personality": actor_profile_json["personality"], 
            "style": actor_profile_json["style"], 
            "occupation": actor_profile_json["occupation"]
        }
        df = pd.DataFrame([
            current_profile,
        ])
        st.data_editor(df)
        return current_profile

    except Exception as e:
        print(e)
        return


@st.cache_data
def show_actor_appearance(current_profile):
    '''
    Step 2: Generate a detailed profile of the character.
    '''
    st.subheader('캐릭터 외형 정보 보기')
    messages = prompt_step_2.get_messages(json.dumps(current_profile))
    response = send_chat(messages)
    response = send_chat(messages)
    try:
        print("Step 2 response")
        print(response)
        actor_detail_json = json.loads(response)
        print(actor_detail_json)
        current_appearance = {
            "appearance": actor_detail_json["appearance"],
            "fashion": actor_detail_json["fashion"],
        }
        st.subheader("외모")
        st.write(actor_detail_json["appearance"])
        st.subheader("스타일")
        st.write(actor_detail_json["fashion"])
        return current_appearance
    except Exception as e:
        print(e)
        return {}

def set_up_default_view():
    st.title('가상 캐스팅')
    user_input = st.text_input('캐릭터의 성격을 알려주세요.', "유튜버 겸 모델 출신 인플루언서 SNS없이 못 사는 인생은 폼생폼사 20대 초반 남자 캐릭터 만들어 줘.")
    current_profile = show_actor_profile(user_input)
    current_appearance = show_actor_appearance(current_profile)


if __name__ == '__main__':
    set_up_default_view()

