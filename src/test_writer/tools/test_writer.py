from openai import OpenAI
from pathlib import Path

client = OpenAI()

# Generate clean test code with no extra text
def write_test_file(code: str, filename: str) -> str:
    prompt = f"""
    You are a professional software test engineer.

    Your task is to write a single JavaScript or TypeScript unit test file with 100% test coverage using the appropriate framework (e.g. Jest or Vitest) for the file below.

    The test file will be saved in the same directory as the source file, so use a relative import like './example' — not '../src/...'.

    Do not include setup instructions, explanations, markdown formatting, or commentary.

    Only return the test code.

    --- SOURCE FILE ({filename}) ---
    {code}
    --- END SOURCE FILE ---
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content.strip()

    # Cleanup: remove ```js or ``` blocks if GPT still returns them
    if output.startswith("```"):
        parts = output.split("```")
        output = parts[1] if len(parts) > 1 else output
        if output.strip().startswith("js") or output.strip().startswith("javascript"):
            output = output.strip().split('\n', 1)[1]

    return output.strip()
