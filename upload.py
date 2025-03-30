from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

filename = "input/ExpertGenQA.pdf"

# file_input = client.files.create(
#     file=open(filename, "rb"),
#     purpose="assistants",
# )

print(client.files.list())

# for file in client.files.list():
#     print(file)
#     client.files.delete(file_id=file.id)