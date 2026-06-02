from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

def determine_urgency(request):

    prompt = f"""
    Determine urgency.

    Return JSON:

    {{
      "urgency":"low|medium|high"
    }}

    Request:
    {request}
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
    return raw_content[start:end+1] if start != -1 and end != -1 else raw_content

if __name__ == "__main__":
    print(
        determine_urgency(
            "My exam starts in 30 minutes and I cannot login."
        )
    )