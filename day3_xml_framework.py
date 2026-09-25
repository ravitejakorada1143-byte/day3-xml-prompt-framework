import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

resume_text = """
K Raviteja
Education = B tech
Email: raviteja@example.com
Skills: Python, JavaScript, Firebase
Experience: GenAI Engineer
"""


def llm_response(resume):

    prompt = f"""
Extract the following information from the resume:

- Name
- Education
- Email
- Primary Skills

Rules:
1. Put the extracted information only between <data> and </data>.
2. Do not add greetings.
3. Do not add explanations.
4. Do not add any text outside the XML tags.

Resume:
{resume}
"""

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a resume information extraction assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"API Error: {e}"


def extract_data(raw_response):

    start_tag = "<data>"
    end_tag = "</data>"

    start_index = raw_response.find(start_tag)
    end_index = raw_response.find(end_tag)

    if start_index == -1 or end_index == -1:
        return "Error: Data tags not found"

    start_index = start_index + len(start_tag)

    extracted_data = raw_response[start_index:end_index]

    return extracted_data.strip()


if __name__ == "__main__":

    print("Starting Day 3 XML extraction...")

    raw_response = llm_response(resume_text)

    print("\nRaw LLM Response:")
    print(raw_response)

    result = extract_data(raw_response)

    print("\nIsolated Data:")
    print(result)