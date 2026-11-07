from openai import OpenAI
from dotenv import load_dotenv
import os

from database import (initialize_database,
                      save_message,
                      load_history
                      )

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_AI_KEY")
)

# Read the system prompt from the file
with open("htb-mentor-prompt.md", "r", encoding="utf-8") as file:
    mentor_prompt = file.read()

# Initialize the database and load the conversation history    
initialize_database()    
history = load_history()
print(f"Loaded {len(history)} messages from database")

# Create the chat loop
while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break
    
    history.append({
        "role": "user",
        "content": user_input
        })
    
    save_message("user", user_input)
    
    messages = [
        {
            "role": "system",
            "content": mentor_prompt
        }   
    ]
    
    # include the conversation history in the messages
    messages.extend(history)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    
       
    # Get the agent's response and print it
    agent_response = response.choices[0].message.content
    print(f"\nHTB Mentor: {agent_response}")
    
    # Append the agent's response to the history
    history.append({
        "role": "assistant",
        "content": agent_response
    })
    save_message("assistant", agent_response)