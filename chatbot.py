from openai import OpenAI

client = OpenAI()

def get_api_chat_response_message(model, messages):

    api_response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    return api_response.choices[0].message.content

model = "gpt-3.5-turbo"

chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

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