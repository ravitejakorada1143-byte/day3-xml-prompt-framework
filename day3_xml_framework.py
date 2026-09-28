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
Education: B.Tech
Email: raviteja@example.com
Skills: Python, JavaScript, Firebase
Experience: 2 years
"""


def get_llm_response(resume):

    prompt = f"""
Read the candidate information provided below and extract these details:

Name
Education
Email
Primary Skills
Experience

Return the result using exactly this structure:

<data>
Name: candidate name
Education: candidate education
Email: candidate email
Primary Skills: candidate skills
Experience: candidate experience
</data>

Rules:
1. The extracted information must be inside <data> and </data>.
2. Do not provide greetings.
3. Do not provide explanations.
4. Do not create information that is missing from the resume.
5. Do not place conversational text outside the XML boundaries.

Candidate Resume:
{resume}
"""

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": "You extract candidate information accurately and follow the requested XML format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"API Error: {error}"


def isolate_data(response_text):

    opening_tag = "<data>"
    closing_tag = "</data>"

    opening_position = response_text.find(opening_tag)
    closing_position = response_text.find(closing_tag)

    if opening_position == -1 or closing_position == -1:
        return "Error: XML data boundaries were not found."

    data_start = opening_position + len(opening_tag)

    extracted_content = response_text[data_start:closing_position]

    return extracted_content.strip()


if __name__ == "__main__":

    print("Starting candidate information extraction...")

    llm_output = get_llm_response(resume_text)

    print("\nRaw LLM Response:")
    print(llm_output)

    clean_data = isolate_data(llm_output)

    print("\nIsolated Candidate Data:")
    print(clean_data)