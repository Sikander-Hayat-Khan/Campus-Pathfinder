from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()


def generate_summary(memory):

    prompt = f"""
    You are a student support assistant.

    Create a concise support ticket summary.

    Information:
    {memory}

    The summary should include:

    - Category
    - Student ID
    - Issue Description
    - Relevant Details
    - Recommended Action

    Keep it professional and under 150 words.
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

    return response.choices[0].message.content