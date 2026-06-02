from openai import OpenAI
import json

client = OpenAI()

def classify_request(user_message):

    prompt = f"""
    Return JSON:

    {{
    "category":"",
    "confidence":0.0
    }}

    Categories:

    login_issue
    registration_issue
    fee_issue
    exam_issue
    other

    Request:

    {user_message}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content