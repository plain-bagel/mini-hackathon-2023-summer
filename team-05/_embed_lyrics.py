import json
import pickle
from pathlib import Path

from _gpt_utils import chat, embed
from _prompt import Prompt

# Get song DB and prompt to extract embeddable context
LYRICS_PROMPT_PATH = Path("prompts/lyrics_prompt.txt")
CRAWLED_DATA_PATH = Path("db/song_db.json")


def main():
    # Read crawled JSON data
    with open(CRAWLED_DATA_PATH, 'r') as file:
        lyrics_db = json.load(file)

    # Extract context from song lyrics
    lyrics_prompt = Prompt(LYRICS_PROMPT_PATH, subs_pattern="<>")

    # Iterate over lyrics in DB and extract context with ChatGPT, then embed it
    lyrics_embs = []
    for lyrics in lyrics_db:
        print(str(len(lyrics_embs)) + ": " + lyrics['title'])

        # Query ChatGPT to extract context from lyrics
        lyrics_prompt.substitute("LYRICS", lyrics['lyrics'])
        lyrics_prompt_str = str(lyrics_prompt).replace("\n", " ")
        msg = [
            {
                "role": "user",
                "content": lyrics_prompt_str
            }
        ]

        try:
            # Extract context with LLM
            lyrics_context = chat(messages=msg, stream=False)
            lyrics_context = lyrics_context['choices'][0]['message']['content']

            # Embed context into 1536-dim vector space
            embedding = embed(prompt=lyrics_context)
            lyrics_embs.append(
                {
                    "title": lyrics['title'],
                    "lyrics": lyrics['lyrics'],
                    "artist": lyrics['artist'],
                    "emb": embedding
                }
            )
        except Exception as e:
            print("error")
            continue

        # Reset prompt for next lyrics
        lyrics_prompt.reset()

    # Save embeddings as a binary file
    print(f"Saving {len(lyrics_embs)} embeddings...")
    with open(Path("db/lyrics_embs.pkl"), 'wb') as f:
        pickle.dump(lyrics_embs, f)


if __name__ == "__main__":
    main()
