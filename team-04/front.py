import streamlit as st

import main

setting = st.text_area("GPT에게 지시할 내용")
prompt = st.text_area("GPT에게 요청할 내용")
global contents
if st.button('GPT 호출 및 트윗하기'):
    if not setting or not prompt:
        st.error('setting 값과 prompt는 필수입니다.', icon="🚨")
    else:
        contents = main.request_chat(setting, prompt)
        print(f"1 : {contents}")
        st.code(contents)
        main.make_tweet(contents)
        # st.button('트윗하기', on_click=main.make_tweet(contents, option))
