"""
Summer 2023 PlainBagel mini-Hackathon
Team 5 - 챗껄룩 -- Song Recommender for Dialogue inputs
Team Members: 최윤종, 이성희, 이예원, 정지은, 방승희, 강지훈*(Hackathon Organizer)
song_recommender.py - Jeehoon Kang
"""

import pickle
import time
from multiprocessing import Manager, Process
from pathlib import Path

import numpy as np
import streamlit as st

from mini_hack.team_05._gpt_utils import chat, embed
from mini_hack.team_05._prompt import Prompt
from mini_hack.team_05 import DB_DIR, PROMPT_DIR

# Paths to prompts and lyrics DB
DIALOGUE_PROMPT_PATH = Path(PROMPT_DIR, "dialogue_prompt.txt")
RECOMMEND_PROMPT_PATH = Path(PROMPT_DIR, "recommendation_prompt.txt")
LYRICS_DB_PATH = Path(DB_DIR, "lyrics_embs.pkl")

LyricsDB = list[dict[str, str | list[float]]]


@st.cache_data
def load_lyrics_db(db_path: Path) -> LyricsDB:
    """
    Load lyrics embedding database
    "emb" - list[float] of length 1536
    returns: list of dictionaries with keys "title", "lyrics", "artist", "emb"
    """
    assert db_path.exists(), "Lyrics DB does not exist"
    with db_path.open("rb") as db_f:
        db: LyricsDB = pickle.load(db_f)
    return db


def get_dialogue_embedding(dialogue: str) -> list[float] | None:
    """
    Use ChatGPT to transform dialogue into full text, and then get embedding of full text
    returns: list[float] of length 1536 representing embedding of full text
    """
    queue = Manager().Queue()
    dialogue = dialogue.replace("\n", " ")
    msg = [{"role": "user", "content": dialogue}]

    # Query ChatGPT
    proc = Process(target=chat, args=(msg, False, queue))
    proc.start()
    try:
        res = queue.get(timeout=10)
        res = res["content"]
        proc.join()
    except Exception as e:
        print("ChatGPT Error: ", e)
        return None

    # Get embedding of response
    proc = Process(target=embed, args=(res, queue))
    proc.start()
    try:
        embedding: list[float] | None = queue.get(timeout=10)
        if embedding is None:
            raise Exception("Embedding is None")
        proc.join()
    except Exception as e:
        print("Embedding Error: ", e)
        return None
    return embedding


def get_embedding_distance(emb1: list[float], emb2: list[float]) -> float:
    """
    Get Euclidean distance between two embeddings
    TODO: Normalize vectors and use cosine distance instead?
    returns: float representing distance between two embeddings
    """
    return float(np.linalg.norm(np.array(emb1) - np.array(emb2)))


def get_recommendation(
    prompts: tuple[Prompt, Prompt], dialogue_input: str, lyrics_db: LyricsDB
) -> tuple[dict, str] | None:
    """
    Full Recommendation Pipeline
    1. Get dialogue embedding
    2. Compare dialogue embedding with lyrics embeddings
    3. Create recommendation reason
    returns: tuple of recommended song info and recommendation reason
    """
    dialogue_prompt, recommend_prompt = prompts
    queue = Manager().Queue()

    # Create dialogue embedding
    with st.spinner("대화를 분석하고 있어요(1/3)..."):
        dialogue_prompt.substitute("DIALOGUE", dialogue_input)
        embedding = get_dialogue_embedding(str(dialogue_prompt))
        if embedding is None:
            st.error("대화를 분석하는데 오류가 발생했어요. 다시 시도해주세요.")
            return None

    # Compare dialogue embedding with lyrics embeddings
    # TODO: For larger DB size, use KDTree or ANN to speed up search
    with st.spinner("대화에 어울리는 노래를 찾고 있어요(2/3)..."):
        time.sleep(2)
        best = {"title": "None", "lyrics": "None", "score": 10000.0}
        for lyric in lyrics_db:
            score = get_embedding_distance(embedding, lyric["emb"])  # type: ignore
            if score < float(best["score"]):  # type: ignore
                best = {
                    "title": lyric["title"],
                    "lyrics": lyric["lyrics"],
                    "score": score,
                }

    # Create recommendation reason
    recommend_data = {
        "DIALOGUE": dialogue_input,
        "LYRICS": best["lyrics"],
    }
    for key, value in recommend_data.items():
        recommend_prompt.substitute(key, str(value))

    # Query ChatGPT for recommendation reason based on dialogue and lyrics
    recommend_prompt_str = str(recommend_prompt).replace("\n", " ")
    msg = [{"role": "user", "content": recommend_prompt_str}]
    with st.spinner("추천 이유를 작성하고 있어요(3/3).."):
        proc = Process(target=chat, args=(msg, False, queue))
        proc.start()
        try:
            rec_reason = queue.get(timeout=25)
            rec_reason = rec_reason["content"]
            proc.join()
        except Exception as e:
            print("ChatGPT Rec. Error: ", e)
            return None

        rec_reason = rec_reason.replace(".", ".\n\n")
    return best, rec_reason


def main() -> None:
    st.title("챗껄룩 🐈‍⬛")
    st.info("🎶 대화 스니핏을 입력하시면, 감정선과 스토리를 분석해 큐레이션된 노래 DB에서 어울리는 노래를 찾아 추천해준답니다!")
    st.markdown("""---""")

    # Load lyrics embedding database
    lyrics_db = load_lyrics_db(LYRICS_DB_PATH)

    # Prepare prompts
    dialogue_prompt = Prompt(DIALOGUE_PROMPT_PATH, subs_pattern="<>")
    recommend_prompt = Prompt(RECOMMEND_PROMPT_PATH, subs_pattern="<>")
    print(f"Dialogue prompt has {dialogue_prompt.subs} required substitutions")
    print(f"Recommendation prompt has {recommend_prompt.subs} required substitutions")

    # Get user input (string representing dialogue)
    dialogue_input = st.text_area("노래 추천을 위한 대화를 입력하세요", height=300)

    # On dialogue input, run recommendation logic
    _, c2 = st.columns([4, 1])
    best, rec_reason = None, None
    if c2.button("노래 추천해줘!", disabled=not dialogue_input):
        # Get recommendation
        rec_result = get_recommendation(
            prompts=(dialogue_prompt, recommend_prompt),
            dialogue_input=dialogue_input,
            lyrics_db=lyrics_db,
        )
        if rec_result is None:
            st.error("대화를 분석하는데 오류가 발생했어요. 다시 시도해주세요.")
            return
        best, rec_reason = rec_result

    if best is not None:
        st.subheader("이 대화와 어울리는 노래는:")
        st.markdown(f"**{best['title']}**")

        st.markdown("""---\n""")
        st.subheader("그 노래는 다음과 같은 가사를 가지고 있어:")
        st.markdown(f"{best['lyrics']}")

        st.markdown("""---\n""")
        st.subheader("이 노래를 추천한 이유는 다음과 같아:")
        st.text(f"{rec_reason}")


if __name__ == "__main__":
    main()
