from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


instruction = """\
添付した論文を以下の項目で要約してください。
各項目ごとに設定されている注意点・文字数に従って記述してください。
1. キーワード: 5つ
2. 背景: 発表時点での研究状況と問題点
    - 5文程度
3. 概要: 論文全体の概要
    - 10文程度
4. 新規性・差分: 他の研究との比較
    - 10文程度
5. 手法: 論文が提案する事項
    - 20文程度
    - 重要な手法やアルゴリズムを含める
    - 一番重要なので詳細に記述
6. 結果: 論文の結果
    - 10文程度
    - 著者が特に重要だと考える結果を記述

各項目は以下のマークダウン形式で記述してください。
# [項目番号]. [項目名]
[記述内容]
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "developer",
            "content": [
                {
                    "type": "text",
                    "text": "出力は日本語で記述し、マークダウン形式としてください。",
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "file",
                    "file": {
                        "file_id": "file-FPdGKcxc58DtVwYdFEoq9T"
                    }
                },
                {
                    "type": "text",
                    "text": instruction,
                }
            ]
        }
    ],
)

print(completion.choices[0].message.content)
