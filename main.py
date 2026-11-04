import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from call_function import available_functions, call_function
from prompts import system_prompt


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
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    for _ in range(20):
        print("new loop")
        response = client.chat.completions.create(
            model="openrouter/free", messages=messages, tools=available_functions
        )

        if not response.usage:
            raise RuntimeError("Usage response invalid")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.type != "function":
                    continue
                result_message = call_function(tool_call, verbose=args.verbose)

                if not result_message["content"]:
                    raise Exception(
                        f"Empty result from function: {tool_call.function.name}"
                    )

                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")

        elif args.verbose == True:
            print(f"User prompt:{args.user_prompt}")
            print(f"Prompt tokens:{response.usage.prompt_tokens}")
            print(f"Response tokens:{response.usage.completion_tokens}")
            print("\n")
            print(response.choices[0].message.content)
            return

        else:
            print(response.choices[0].message.content)
            return

    print("Reached maximum number of iterations")
    sys.exit(1)


if __name__ == "__main__":
    main()
