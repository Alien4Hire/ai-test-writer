from openai import OpenAI

client = OpenAI()

# Repair a broken test file based on failure error logs
def repair_tests(code: str, test_code: str, error: str) -> str:
    prompt = f"""
You're a senior developer helping to fix a broken test file.

Below is the source file, a failing test file, and the error message. Please rewrite the test file to pass, while still achieving full coverage.

--- BEGIN SOURCE FILE ---
{code}
--- END SOURCE FILE ---

--- BEGIN TEST FILE ---
{test_code}
--- END TEST FILE ---

--- ERROR MESSAGE ---
{error}
--- END ERROR ---

Return only the fixed test code.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
