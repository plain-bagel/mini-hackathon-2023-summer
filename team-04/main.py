# mypy: ignore-errors
import os

import openai
import tweepy
from dotenv import load_dotenv


def request_chat(setting, prompt):
    load_dotenv("키 파일 경로")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": setting},
            {"role": "user", "content": prompt},
        ],
    )
    return response["choices"][0]["message"]["content"]


def make_tweet(contents):
    (
        twitter_key,
        twitter_key_secret,
        twitter_access_token,
        twitter_access_token_secret,
        twitter_access_bearer_token,
    ) = get_twitter_key()
    client = tweepy.Client(
        bearer_token=twitter_access_bearer_token,
        consumer_key=twitter_key,
        consumer_secret=twitter_key_secret,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
    )
    client.create_tweet(text=contents)


def get_twitter_key():
    load_dotenv("키 파일 경로")
    twitter_key = os.getenv("TWITTER_API_KEY")
    twitter_key_secret = os.getenv("TWITTER_API_KEY_SECRET")
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    twitter_access_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    return (
        twitter_key,
        twitter_key_secret,
        twitter_access_token,
        twitter_access_token_secret,
        twitter_access_bearer_token,
    )


if __name__ == "__main__":
    # 아래 코드는 테스트를 돌릴때만 사용
    load_dotenv("키파일 경로")
    setting = "1. 트위터의 글은 100자 이내로 작성되어야만 한다. 2. 너는 안드로이드 개발자이다."
    prompt = "개발에 도움이 되는 트위터 글을 만들어줘. 100자 이내로 만들어줘"
    contents = request_chat(setting, prompt)
    make_tweet(contents)
