import openai
import json

with open('secrets.json') as f:
    secrets = json.load(f)

openai.api_key = secrets['openai_api_key']

