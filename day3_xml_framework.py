resume_text = """
K Raviteja
Email: raviteja@example.com
Skills: Python, JavaScript, Firebase
Experience: GenAI Engineer
"""


def mock_llm_response(resume):
    return """
Sure! Here is the extracted information:

<data>
Name: K Raviteja
Email: raviteja@example.com
Primary Skills: Python, JavaScript, Firebase
</data>

Let me know if you need anything else!
"""


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

    raw_response = mock_llm_response(resume_text)

    print("\nRaw LLM Response:")
    print(raw_response)

    result = extract_data(raw_response)

    print("\nIsolated Data:")
    print(result)