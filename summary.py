from openai import OpenAI
import os
import json
import pprint

from dotenv import load_dotenv

load_dotenv()

from schema import SectionSchema, KeywordsSchema

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
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file": {"file_id": "file-RinaaMjubEnqi4dVP7gCNs"},
                    },
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                ],
            },
        ],
        response_format={"type": "json_schema", "json_schema": json_schema},
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

# Response format: Use given Json schema
section.title: 概要
section.contents: 論文中の「abstract/summary/background」の要約
section.subsections: empty
"""

json_schema = {
    "name": "document_schema",
    "strict": True,
    "schema": SectionSchema.model_json_schema(),
}

result = file_analyze(system_prompt, user_prompt, json_schema)
pprint.pprint(result)

user_prompt = """\
# Task: Generate summary from Thesis/Paper/Article
このセクションは「手法」セクションに相当します。
論文が提案している概念・手法・実施した実験について、論文の論述の流れを基に詳しく教えてください。
読みやすいように、構造的な文章で要約してください。

# Output format: Use given Json schema
section.title: 手法
section.contents: 論文中の「手法」の概要
section.subsections: 論文中の「手法」の各サブセクションの概要
section.subsections[].title: サブセクションのタイトル
section.subsections[].contents: サブセクションの概要
"""

json_schema = {
    "name": "document_schema",
    "strict": True,
    "schema": SectionSchema.model_json_schema(),
}

result = file_analyze(system_prompt, user_prompt, json_schema)
pprint.pprint(result)

user_prompt = """\
# Task: Generate summary from Thesis/Paper/Article
このセクションは「新規性・差分」セクションに相当します。
論文中で述べられる既存手法との違いや提案手法のメリット・デメリットを基に詳しくまとめてください。
読みやすいように、構造的な文章で要約してください。

# Output format: Use given Json schema
section.title: 新規性・差分
section.contents: 論文中の「新規性・差分」の概要
section.subsections: 「新規性・差分」の各サブセクション
section.subsections[].title: サブセクションのタイトル
section.subsections[].contents: サブセクションの概要
"""

json_schema = {
    "name": "document_schema",
    "strict": True,
    "schema": SectionSchema.model_json_schema(),
}

result = file_analyze(system_prompt, user_prompt, json_schema)
pprint.pprint(result)

user_prompt = """\
# Task: Generate summary from Thesis/Paper/Article
このセクションは「結果」セクションに相当します。
論文中で述べられる実験結果や評価結果を基に詳しくまとめてください。
特に、筆者が強調しているポイントや、実験結果の解釈についても詳しく教えてください。
読みやすいように、構造的な文章で要約してください。

# Output format: Use given Json schema
section.title: 結果
section.contents: 論文中の「結果」の概要
section.subsections: 「結果」の各サブセクション
section.subsections[].title: サブセクションのタイトル
section.subsections[].contents: サブセクションの概要
"""

json_schema = {
    "name": "document_schema",
    "strict": True,
    "schema": SectionSchema.model_json_schema(),
}

result = file_analyze(system_prompt, user_prompt, json_schema)
pprint.pprint(result)

system_prompt = """\
# Task: Thesis/Paper/Article analysis
論文の添付ファイルを基に、ユーザーの命令に従って論文から情報を要約・抽出してください。
"""

user_prompt = """\
# Task: Extract keywords or topics from Thesis/Paper/Article
この論文のキーワードやトピックを抽出してください。

# # Output format: Use given Json schema
{
    "keywords": [
        "keyword1",
        "keyword2",
        ...
    ]
}
"""

json_schema = {
    "name": "document_schema",
    "strict": True,
    "schema": KeywordsSchema.model_json_schema(),
}

result = file_analyze(system_prompt, user_prompt, json_schema)
pprint.pprint(result)
print(KeywordsSchema.model_validate(result))
