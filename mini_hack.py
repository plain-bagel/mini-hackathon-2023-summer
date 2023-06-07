import os

import openai
from dotenv import load_dotenv

import multiprocessing


# Load Environment variables and have them as constants
load_dotenv()

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


def embed(prompt, queue=None):
    """
    Generate embeddings using OpenAI Embedding API
    """
    prompt = prompt.replace("\n", " ")
    try:
        gpt_res = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=[prompt],
        )
    except Exception as e:
        print(e)
        if queue is not None:
            queue.put(None)
        return None

    # Add to queue (for inter-process communication)
    if queue is not None:
        queue.put(gpt_res['data'][0]['embedding'])
    return gpt_res['data'][0]['embedding']


def main():
    # Single prompt example
    prompt = "Can you give me one tip(in less than 10 words) for a healthy lifestyle?"
    msg = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    """
        # Prompt with history (아마 이렇게는 거의 안쓸 듯 합니다)
        msg = [
            {
                "role": "user",
                "content": "Can you give me one tip(in less than 10 words) for a healthy lifestyle?"
            },
            {
                "role": "bot",
                "content": "Eat healthy food"
            },
            {
                "role": "user",
                "content": prompt2
            }
        ]
    """

    manager = multiprocessing.Manager()
    queue = manager.Queue()
    p = multiprocessing.Process(target=chat, args=(msg, True, queue))
    p.start()
    response = ""
    while True:
        try:
            chunk = queue.get(timeout=3)
            if chunk == {}:
                break
            if 'content' in chunk:
                response += chunk['content']
                print(response)
        except Exception as e:
            continue
    p.join(timeout=30)
    print(f"Full response: {response}\n\n")

    # Embedding example
    prompt1 = "apples are tasty and they are my favorite fruit"
    prompt2 = "I love apples"
    prompt3 = "I have a pet dog named walnut"

    embedding1 = embed(prompt1)
    embedding2 = embed(prompt2)
    embedding3 = embed(prompt3)
    print(f"The embeddings are of type {type(embedding1)} and their elements are of type {type(embedding1[0])}\n\n")

    # Useful: Compare vector space distances (Euclidean / Cosine)
    import numpy as np
    np_emb1, np_emb2, np_emb3 = np.array(embedding1), np.array(embedding2), np.array(embedding3)
    print(f"Distance between embedding1 and embedding2: {np.linalg.norm(np_emb1 - np_emb2)}")
    print(f"Distance between embedding1 and embedding3: {np.linalg.norm(np_emb1 - np_emb3)}")
    print(f"Distance between embedding2 and embedding3: {np.linalg.norm(np_emb2 - np_emb3)}")
    # 코사인 거리를 활용하고 싶으면 scipy.spatial.distance.cosine을 사용하면 된다.
    # (1, 2)는 맥락적으로 가깝지만, (1, 3)이나 (2, 3)은 맥락적으로 가깝지 않음을 볼 수 있다.
    # 이를 활용한 텍스트 데이터베이스에서의 색출 / 쿼리에 따른 추천 랭킹 등을 매길 수 있다.


if __name__ == "__main__":
    main()
