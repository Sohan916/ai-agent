import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("api key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not response.usage:
        raise RuntimeError("Usage response invalid")

    if args.verbose == True:
        print(f"User prompt:{args.user_prompt}")
        print(f"Prompt tokens:{response.usage.prompt_tokens}")
        print(f"Response tokens:{response.usage.completion_tokens}")
        print("/n")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
