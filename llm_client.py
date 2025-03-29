from google import genai
import os, re

gemini = genai.Client(api_key=os.environ['GEMINI_KEY'])


def call_gemini(prompt: str) -> str:
    response = gemini.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt
    )
    response = response.text
    match = re.search(r'\[.*\]', response, re.DOTALL)
    response_cleaned = response[match.start():match.end()] if match else ""

    return response_cleaned


if __name__ == '__main__':
    # Example usage
    from schedule.prompts import timestamp_prompt

    tasks = ['Make bed', 'Wash dishes', 'Wipe down kitchen counters', 'Sweep kitchen floor', 'Clean microwave', 'Vacuum living room', 'Dust living room furniture', 'Clean bathroom sink and mirror', 'Scrub toilet', 'Take out trash and recycling']
    llm_response = eval(call_gemini(timestamp_prompt.format(tasks=tasks)))
    print(llm_response)
