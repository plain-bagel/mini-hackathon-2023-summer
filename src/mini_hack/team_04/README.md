# 주사친 트위터 봇

> 🕹️ 주사친 트위터 봇은 OpenAI의 GPT API를 활용하여, 사용자가 원하는 캐릭터의 트윗할 내용을 만들어주고, 미리 만들어 놓은 트위터 계정에 트윗할 수 있는 서비스

## Environments

`~/mini-hackathon-2023-summer/team-04`에 `.env` 파일을 추가합니다.
`.env` 는 아래 항목을 반드시 포함해야합니다.


```dotenv
OPENAI_API_KEY=<YOUR_API_KEY>
TWITTER_API_KEY=<트위터에서 발급 받은 API 키> 
TWITTER_API_KEY_SECRET=<트위터에서 발급 받은 API 시크릿>
TWITTER_ACCESS_TOKEN=<트위터에서 발급 받은 ACCESS_TOKEN>
TWITTER_ACCESS_TOKEN_SECRET=<트위터에서 발급 받은 ACCESS_TOKEN_SECRET>
TWITTER_BEARER_TOKEN=<트위터에서 발급 받은 BEARER_TOKEN>
```

`OPENAI_API_KEY`는 [OpenAI](https://platform.openai.com/account/api-keys)에서 발급받을 수 있습니다.

`트위터 관련 키`는 [Developer Portal](https://developer.twitter.com/en/portal/dashboard)에서 발급받을 수 있습니다.
```dotenv
발급 시 주의 사항
Developer Portal에서 Projects & Apps 클릭 > 프로젝트 클릭 > User authentication settings
 edit 클릭 > Read and write and Direct message 클릭 > App info
Callback URI / Redirect URL에 https://localhost 입력 > Website URL에  https://localhost.com 입력 > save
이후 다시 프로젝트로 돌아가 keys and tokens 클릭 > 관련 키 저장
```



## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run front.py
```

## See more

- [파멸의 4오정 아이디어 회의록 및 프롬프트](https://www.notion.so/plainbagel/4b9131ab1cbe4655b41fc0fa825af91c?pvs=4)
- [June 2023 PlainBagel AI mini-Hackathon](https://www.notion.so/plainbagel/June-2023-PlainBagel-AI-mini-Hackathon-84def79c77064bc399a07a8b54c78205)
