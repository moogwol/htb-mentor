from ai.client import ask_ai
from database.messages import add_message, get_messages


def send_message(conversation_id, prompt):
    messages = get_messages(conversation_id)

    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in messages
    ]

    response = ask_ai(prompt, history)

    add_message(conversation_id, "user", prompt)
    add_message(conversation_id, "assistant", response)

    return response