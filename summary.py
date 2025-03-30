from openai import OpenAI
import os
import json
import pprint

from dotenv import load_dotenv
load_dotenv()

from schema import DocumentSchema, SectionSchema

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def file_analyze(system_prompt, user_prompt, json_schema) -> None:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt,
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file": {
                            "file_id": "file-RinaaMjubEnqi4dVP7gCNs"
                        }
                    },
                    {
                        "type": "text",
                        "text": user_prompt,
                    }
                ]
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": json_schema
        }
    )

    return json.loads(completion.choices[0].message.content)


system_prompt = """\
# Task: Thesis/Paper/Article analysis
論文の添付ファイルを基に、ユーザーの命令に従って論文から情報を要約・抽出してください。

# Response format: Use given Json schema
論文の要約をJson schemaに従って出力してください。

# Language: Japanese
項目名や内容は日本語で記載してください。ただし、論文中にある英語の用語はそのまま使用してください。

# Background: Making a summary report of the thesis
ユーザーの論文の要約レポートを補助して下さい。
"""

user_prompt = """\
# Task: Generate summary from Thesis/Paper/Article
この論文の概要について教えてください。
このセクションは「概要」セクションに相当します。
ここでは構造的な文章よりも、論文全体の流れをつかめるような要約をしてください。
"""

json_schema = {
    "name": "document_schema",
    "strict": True,
    "schema": SectionSchema.model_json_schema(),
}

result = file_analyze(system_prompt, user_prompt, json_schema)

pprint.pprint(result)