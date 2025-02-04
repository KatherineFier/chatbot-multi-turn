from openai import OpenAI
import tiktoken
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='chatbot.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger.debug('This message should go to the log file')

logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

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
        total_prompt_tokens = sum(entry.get("prompt_token_count", 0) for entry in chat_history)
        total_response_tokens = sum(entry.get("response_token_count", 0) for entry in chat_history)
        logger.info(f"Total prompt tokens: {total_prompt_tokens}")
        logger.info(f"Total response tokens: {total_response_tokens}")
        logger.info(f"Total tokens used: {total_prompt_tokens + total_response_tokens}")
        break


    prompt_token_count = len(encoding.encode(user_input))
    # print(token_count)

    if (prompt_token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue

    chat_history.append({
        "role": "user",
        "content": user_input,
        "prompt_token_count": prompt_token_count
    })

    response = get_api_chat_response_message(model, chat_history)

    response_token_count = len(encoding.encode(response))

    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": response,
        "response_token_count": response_token_count
    })


