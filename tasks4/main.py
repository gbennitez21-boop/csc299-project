import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

paragraphs = [
    "Today I need to finish assembling my PKMS semester project, record the demo video, upload everything to GitHub, and make sure the timeline is documented clearly.",
    "I should revise my personal notes from last week, reorganize my tasks by energy level, and check which assignments are approaching their deadlines."
]

def summarize(text: str) -> str:
    return text[:40] + "..."


def main():
    print("Summaries:\n")
    for p in paragraphs:
        short = summarize(p)
        print(f"- {short}")

if __name__ == "__main__":
    main()
