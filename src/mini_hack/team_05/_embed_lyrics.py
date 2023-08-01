import json
import pickle
from pathlib import Path

from mini_hack.team_05._gpt_utils import chat, embed
from mini_hack.team_05._prompt import Prompt
from mini_hack.team_05 import DB_DIR, PROMPT_DIR

# Get song DB and prompt to extract embeddable context
LYRICS_PROMPT_PATH = Path(PROMPT_DIR) / "lyrics_prompt.txt"
CRAWLED_DATA_PATH = Path(DB_DIR) / "song_db.json"


def main() -> None:
    # Read crawled JSON data
    with CRAWLED_DATA_PATH.open() as file:
        lyrics_db = json.load(file)

    # Extract context from song lyrics
    lyrics_prompt = Prompt(LYRICS_PROMPT_PATH, subs_pattern="<>")

    # Iterate over lyrics in DB and extract context with ChatGPT, then embed it
    lyrics_embs: list[dict[str, str | list[float]]] = []
    for lyrics in lyrics_db:
        print(str(len(lyrics_embs)) + ": " + lyrics["title"])

        # Query ChatGPT to extract context from lyrics
        lyrics_prompt.substitute("LYRICS", lyrics["lyrics"])
        lyrics_prompt_str = str(lyrics_prompt).replace("\n", " ")
        msg = [{"role": "user", "content": lyrics_prompt_str}]

        try:
            # Extract context with LLM
            lyrics_context = chat(messages=msg, stream=False)
            if lyrics_context is None:
                print("error, skipping song")
                continue
            lyrics_context_str: str = lyrics_context["choices"][0]["message"]["content"]

            # Embed context into 1536-dim vector space
            embedding = embed(prompt=lyrics_context_str)
            if embedding is None:
                print("error, skipping song")
                continue
            lyrics_embs.append(
                {
                    "title": lyrics["title"],
                    "lyrics": lyrics["lyrics"],
                    "artist": lyrics["artist"],
                    "emb": embedding,
                }
            )
        except Exception:
            print("error")
            continue

        # Reset prompt for next lyrics
        lyrics_prompt.reset()

    # Save embeddings as a binary file
    print(f"Saving {len(lyrics_embs)} embeddings...")
    with (Path(DB_DIR) / "lyrics_embs.pkl").open("wb") as f:
        pickle.dump(lyrics_embs, f)


if __name__ == "__main__":
    main()
