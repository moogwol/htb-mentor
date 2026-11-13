from ai.client import ask_ai

from database.conversations import (
    create_conversation,
    get_conversation,
)

from database.messages import (
    add_message,
    get_messages,
)

def select_conversation():
    choice = input(
        "Enter conversation ID or 0 to start a new conversation: "
        )
    
    if choice == "0":
        machine_id = int(input("Enter HTB machine ID: "))
        title = input("Enter conversation title: ")
        
        conversation_id = create_conversation(machine_id, title)
        return conversation_id
    
    conversation_id = int(choice)
    conversation = get_conversation(conversation_id)
    
    if conversation is None:
        print("Conversation not found. ")
        return None

def chat(conversation_id):
    stored_messages = get_messages(conversation_id) 
    
    # Only send role and content to the AI, not the message ID or conversation ID
    history = [{"role": message["role"], "content": message["content"]} for message in stored_messages]   

    print("\nHTB Mentor rady. Type 'exit' or 'bye' to end the conversation.")

    while True:
        prompt = input("\nYou: ").strip()
        
        if prompt.lower() in ["exit", "bye"]:
            print("HTB Mentor: Goodbye!")
            break
        
        if not prompt:
            continue
        
        try:
            response = ask_ai(prompt, history)
       
            
            # Save both sides of the conversation to the database
            add_message(conversation_id, "user", prompt)
            add_message(conversation_id, "assistant", response)  
            
            print(f"\nHTB Mentor: {response}")
            
        except Exception as error:
            print(f"\nOh shit! Something went wrong: {error}")    
        
        
        
def main():
    conversation_id = select_conversation()
    
    if conversation_id is not None:
        chat(conversation_id)
        
if __name__ == "__main__":
    main()             