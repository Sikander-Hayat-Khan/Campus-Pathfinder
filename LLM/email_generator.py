from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()


def generate_email(
    department,
    summary
):

    prompt = f"""
    Generate a professional support email.

    Department:
    {department}

    Ticket Summary:
    {summary}

    Requirements:

    - Professional tone
    - Clear subject line
    - Concise
    - Ready to send

    Format:

    Subject:
    ...

    Body:
    ...
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