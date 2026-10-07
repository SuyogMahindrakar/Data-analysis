from google import genai


# ---------------------------------------------------
# Create Gemini Client
# ---------------------------------------------------

def get_client(api_key):
    return genai.Client(api_key=api_key)


# ---------------------------------------------------
# Generate Python Code
# ---------------------------------------------------

def generate_python_code(api_key, dataset_info, question):

    client = get_client(api_key)

    prompt = f"""
You are an expert Python Data Analyst.

The pandas DataFrame is already loaded and is named df.

Dataset Information:

{dataset_info}

User Question:
{question}

Generate ONLY executable Python code.

Rules:

1. Use ONLY pandas, numpy and matplotlib.
2. Do NOT import streamlit.
3. Do NOT load any CSV or Excel.
4. Do NOT create another dataframe.
5. Use the existing dataframe named df.
6. Store the final answer in a variable called result.
7. If a chart is required:
      - Create matplotlib figure
      - Store it in variable fig
8. Never use print().
9. Never explain the code.
10. Return ONLY Python code.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    code = response.text.strip()

    # Remove markdown if Gemini returns ```python
    code = code.replace("```python", "")
    code = code.replace("```", "")

    return code.strip()


# ---------------------------------------------------
# Explain Result
# ---------------------------------------------------

def explain_result(api_key, question, result):

    client = get_client(api_key)

    prompt = f"""
You are a professional Data Analyst.

User Question:

{question}

Analysis Result:

{str(result)}

Explain the answer in simple English.

Keep it under 150 words.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()


# ---------------------------------------------------
# Suggest Questions
# ---------------------------------------------------

def suggest_questions(api_key, dataset_info):

    client = get_client(api_key)

    prompt = f"""
Dataset:

{dataset_info}

Suggest 10 interesting questions
a business user can ask.

Only return the questions.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()


# ---------------------------------------------------
# Generate Chart Title
# ---------------------------------------------------

def generate_chart_title(api_key, question):

    client = get_client(api_key)

    prompt = f"""
Generate a short chart title.

Question:

{question}

Return only the title.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()