import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

VALID_CATEGORIES = {
    "login_issue",
    "registration_issue",
    "fee_issue",
    "exam_issue",
    "other"
}


def classify_request(user_message):

    prompt = f"""
Classify the student support request into one of the following categories:
- login_issue
- registration_issue
- fee_issue
- exam_issue
- other

Return JSON:

{{
    "category":"",
    "confidence":0.0
}}

Request:
{user_message}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    raw_content = response.choices[0].message.content
    start = raw_content.find('{')
    end = raw_content.rfind('}')
    raw_content = raw_content[start:end+1] if start != -1 and end != -1 else raw_content
    result = json.loads(raw_content)

    if result["category"] not in VALID_CATEGORIES:

        result["category"] = "other"

    return json.dumps(result)