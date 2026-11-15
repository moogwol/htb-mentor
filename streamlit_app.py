
import streamlit as st
import tempfile
from pathlib import Path

from database.conversations import get_all_conversations, create_conversation
from database.messages import get_messages
from database.machines import get_all_machines
from database.writeups import get_writeups_by_machine
from knowledge_base.importer import import_writeup
from app.chat import send_message


# Set page configuration
st.set_page_config(
    page_title="HTB Mentor",
    page_icon="🤖",
    layout="wide"
)

st.title("HTB Mentor")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Chat", "Knowledge Base"]
)


# ==========================================
# CHAT
# ==========================================

if page == "Chat":


    st.sidebar.header("Conversations")

    # Create a new conversation
    machines = get_all_machines()

    if machines:
        machine_options = {
            machine["name"]: machine["id"]
            for machine in machines
        }

        with st.sidebar.expander("New conversation"):
            with st.form("new_conversation_form"):

                selected_machine = st.selectbox(
                    "Select HTB machine",
                    options=list(machine_options.keys())
                )

                title = st.text_input("Conversation title")
                submitted = st.form_submit_button("Create conversation")
                
                if submitted:
                    if not title.strip():
                        st.error("Please enter a conversation title.")
                    else:
                        create_conversation(
                            machine_options[selected_machine],
                            title.strip()
                        )
                        
                        st.rerun()
    else:
        st.sidebar.warning("No machines found. Add a machine first.")                    
                     
    conversations = get_all_conversations()

    conversation_id = None

    if conversations:
        conversation_options = {
            f"{c['title']} (ID: {c['id']})": c['id']
            for c in conversations
        }

        selected_conversation = st.sidebar.selectbox(
            "Select a conversation",
            options=list(conversation_options.keys())
        )

        conversation_id = conversation_options[selected_conversation]

        st.header(selected_conversation)

        messages = get_messages(conversation_id)

        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    else:
        st.sidebar.write("No conversations found.")
        st.info("No conversations available yet.")

    if conversation_id is not None:
        prompt = st.chat_input(
            "Salaam, what is your question master?..."
        )

        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = send_message(conversation_id, prompt)

                st.markdown(response)


# ==========================================
# KNOWLEDGE BASE
# ==========================================

elif page == "Knowledge Base":

    st.header("Knowledge Base")
    st.write("Import and manage HTB machine walkthroughs.")

    machines = get_all_machines()

    if not machines:
        st.warning("No machines found. Add a machine first.")

    else:

        machine_options = {
            machine["name"]: machine["id"]
            for machine in machines
        }

        st.subheader("Import walkthrough")

        with st.form("import_writeup_form"):

            selected_machine = st.selectbox(
                "HTB Machine",
                options=list(machine_options.keys())
            )

            title = st.text_input(
                "Walkthrough title"
            )

            source = st.text_input(
                "Source URL (optional)"
            )

            uploaded_file = st.file_uploader(
                "Upload walkthrough",
                type=["pdf", "md", "txt"]
            )

            submitted = st.form_submit_button(
                "Import walkthrough"
            )

            if submitted:

                if not title.strip():
                    st.error("Please enter a walkthrough title.")

                elif uploaded_file is None:
                    st.error("Please select a file.")

                else:
                    try:

                        with tempfile.TemporaryDirectory() as temp_dir:

                            file_path = Path(temp_dir) / uploaded_file.name
                            file_path.write_bytes(uploaded_file.getvalue())

                            writeup_id = import_writeup(
                                machine_id=machine_options[selected_machine],
                                file_path=file_path,
                                title=title.strip(),
                                source=source.strip() or None
                            )

                        st.success(
                            f"Walkthrough imported successfully! ID: {writeup_id}"
                        )

                    

                    except (ValueError, FileNotFoundError) as error:
                        st.error(str(error))

        # Display existing walkthroughs

        st.divider()
        st.subheader("Stored walkthroughs")

        selected_machine_for_list = st.selectbox(
            "Select machine to view walkthroughs",
            options=list(machine_options.keys()),
            key="view_machine"
        )

        writeups = get_writeups_by_machine(
            machine_options[selected_machine_for_list]
        )

        if writeups:

            for writeup in writeups:
                with st.expander(writeup["title"]):

                    st.caption(f"Write-up ID: {writeup['id']}")

                    if writeup["source"]:
                        st.markdown(
                            f"Source: {writeup['source']}"
                        )

                    st.markdown(writeup["content"])

        else:
            st.info("No walkthroughs stored for this machine yet.")
