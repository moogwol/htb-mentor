from ai.client import ask_ai
from database.messages import add_message, get_messages
from database.conversations import get_conversation
from knowledge_base.retriever import get_machine_knowledge


def send_message(conversation_id, prompt):
    messages = get_messages(conversation_id)

    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in messages
    ]

    # Retrieve the conversation and its associated machine
    conversation = get_conversation(conversation_id)


    context = None
    
    if conversation:
        knowledge = get_machine_knowledge(conversation["machine_id"])
        
        
        if knowledge:
            machine = knowledge["machine"]
            
            context = f"""
            Machine: {machine["name"]}
            Operating System: {machine["os"]}
            Difficulty: {machine["difficulty"]}
            """

            for writeup in knowledge["writeups"]:
                context += f"""
                Write-up {writeup["title"]}
                {writeup["content"]}
                """
    
    # print("Context being sent to AI:", context)
                
    response = ask_ai(prompt, history, context)

    add_message(conversation_id, "user", prompt)
    add_message(conversation_id, "assistant", response)

    return response