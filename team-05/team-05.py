from mini_hack import chat, embed
import json
import pickle

prompt = "Summarize the mood and story of <LYRICS> in two sentences.  add no explanations."

file_path = "./song_db.json"

lembs = []
with open(file_path, 'r') as file:
    lyrics_db = json.load(file)

    for lyrics in lyrics_db:
        print(str(len(lembs)) + ": " + lyrics['title'])
        prompt = prompt.replace("<LYRICS>", lyrics['lyrics'])

        msg = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        res = chat(messages=msg, stream=False)
        
        try:
            print(res['choices'][0]['message']['content'])
            mood_json = res['choices'][0]['message']['content']
            embedding = embed(prompt=mood_json)
            lembs.append({"title": lyrics['title'], "lyrics": lyrics['lyrics'], "artist": lyrics['artist'], "emb": embedding})        
        except Exception as e:
            print("error")
            continue

with open("lembs.pkl", 'wb') as f:
    pickle.dump(lembs, f)
    
with open("lembs.pkl", "rb") as f:
    lembs = pickle.load(f)
    
    prompt = "너는 짧은 대화를 주면, 대화의 분위기, 정서, 스토리에 맞는 가사를 지닌 노래를 추천해주는 ai야. json 형식으로 나타내주길 바라.\n1. 노래 이름 - 가수\n2. 가사\n3. 대화 분위기 키워드\n4. 가사 분위기 키워드\n5. 노래 추천 이유\n6. 추천 멘트\n- 추천 멘트는 50자 이내여야 해.\n- 키워드는 5개 이내여야 해.\n- 대화는 이거야:\n<대화>"
    msg = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    res = chat(messages=msg, stream=False)
    print(res)