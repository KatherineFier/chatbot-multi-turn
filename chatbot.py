from openai import OpenAI
import tiktoken

client = OpenAI()


def get_api_chat_response_message(model, messages):
    api_response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    # print(api_response)

    return api_response.choices[0].message.content


model = "gpt-3.5-turbo"

encoding = tiktoken.encoding_for_model(model)

token_input_limit = 12289

print(encoding)

chat_history = []

while True:
    if len(chat_history) == 0:
        user_input = input("Hello! You can can type exit at anytime to end this chat. What is your name? ")
    else:
        user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    token_count = len(encoding.encode(user_input))
    # print(token_count)

    if (token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = get_api_chat_response_message(model, chat_history)

    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": response
    })
