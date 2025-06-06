import ollama
import streamlit as st
import torch
import json
import os
from datetime import datetime
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Enhanced Ollama Chatbot",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark/light mode toggle
def load_custom_css(theme_mode: str):
    if theme_mode == "Dark":
        css = """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .sidebar .sidebar-content {
            background-color: #262730;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .user-message {
            background-color: #2b313e;
            border-left: 4px solid #00d4aa;
        }
        .assistant-message {
            background-color: #1e2029;
            border-left: 4px solid #ff6b6b;
        }
        .system-prompt-box {
            background-color: #2b313e;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #464c5c;
        }
        </style>
        """
    else:
        css = """
        <style>
        .stApp {
            background-color: #ffffff;
            color: #262730;
        }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .user-message {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .assistant-message {
            background-color: #f3e5f5;
            border-left: 4px solid #9c27b0;
        }
        .system-prompt-box {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# Chat history management
HISTORY_DIR = "chat_history"
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def save_chat_history(messages: List[Dict], filename: str = None):
    """Save chat history to a JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{timestamp}.json"
    
    filepath = os.path.join(HISTORY_DIR, filename)
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages,
        "model": st.session_state.get("model", ""),
        "system_prompt": st.session_state.get("system_prompt", "")
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chat_data, f, indent=2, ensure_ascii=False)
    
    return filename

def load_chat_history(filename: str):
    """Load chat history from a JSON file"""
    filepath = os.path.join(HISTORY_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading chat history: {str(e)}")
        return None

def get_saved_chats():
    """Get list of saved chat files"""
    if not os.path.exists(HISTORY_DIR):
        return []
    return [f for f in os.listdir(HISTORY_DIR) if f.endswith('.json')]

def export_chat_as_markdown(messages: List[Dict], filename: str = None):
    """Export chat history as markdown"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_export_{timestamp}.md"
    
    markdown_content = f"# Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if st.session_state.get("system_prompt"):
        markdown_content += f"**System Prompt:** {st.session_state['system_prompt']}\n\n"
    
    markdown_content += f"**Model:** {st.session_state.get('model', 'Unknown')}\n\n"
    markdown_content += "---\n\n"
    
    for message in messages:
        role = message['role'].title()
        content = message['content']
        markdown_content += f"## {role}\n\n{content}\n\n"
    
    filepath = os.path.join(HISTORY_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return filename

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "model" not in st.session_state:
    st.session_state["model"] = ""

if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Light"

if "auto_save" not in st.session_state:
    st.session_state["auto_save"] = True

# Sidebar configuration
with st.sidebar:
    st.title("🦙 Enhanced Ollama Chatbot")
    
    # Theme toggle
    st.subheader("🎨 Theme")
    theme_mode = st.selectbox(
        "Choose theme:",
        ["Light", "Dark"],
        index=0 if st.session_state["theme_mode"] == "Light" else 1,
        key="theme_selector"
    )
    st.session_state["theme_mode"] = theme_mode
    
    st.divider()
    
    # Model selection
    st.subheader("🤖 Model Configuration")
    try:
        models = [model["name"] for model in ollama.list()["models"]]
        if models:
            st.session_state["model"] = st.selectbox("Choose your model:", models)
        else:
            st.error("No Ollama models found! Please install models first.")
            st.code("ollama pull llama2")
    except Exception as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        st.info("Make sure Ollama is running: `ollama serve`")
    
    st.divider()
    
    # System prompt configuration
    st.subheader("⚙️ System Prompt")
    system_prompt_presets = {
        "Default": "",
        "Helpful Assistant": "You are a helpful, harmless, and honest assistant. Provide clear and concise answers.",
        "Code Assistant": "You are an expert programmer. Help with coding questions, debugging, and best practices.",
        "Creative Writer": "You are a creative writing assistant. Help with storytelling, poetry, and creative content.",
        "Teacher": "You are a patient teacher. Explain concepts clearly with examples and analogies.",
        "Pirate": "Ahoy! You be a helpful pirate assistant, matey! Speak like a pirate in all yer responses, arrr!",
        "Philosopher": "You are a wise philosopher. Provide thoughtful, deep responses with philosophical insights.",
        "Custom": "custom"
    }
    
    preset_choice = st.selectbox("System prompt preset:", list(system_prompt_presets.keys()))
    
    if preset_choice == "Custom":
        system_prompt = st.text_area(
            "Enter custom system prompt:",
            value=st.session_state["system_prompt"],
            height=100,
            placeholder="Enter your custom system prompt here..."
        )
    else:
        system_prompt = system_prompt_presets[preset_choice]
        if preset_choice != "Default":
            st.info(f"Using preset: {preset_choice}")
    
    st.session_state["system_prompt"] = system_prompt
    
    st.divider()
    
    # Chat history management
    st.subheader("💾 Chat History")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Chat", use_container_width=True):
            if st.session_state["messages"]:
                filename = save_chat_history(st.session_state["messages"])
                st.success(f"Chat saved as: {filename}")
            else:
                st.warning("No messages to save!")
    
    with col2:
        if st.button("📄 Export MD", use_container_width=True):
            if st.session_state["messages"]:
                filename = export_chat_as_markdown(st.session_state["messages"])
                st.success(f"Exported as: {filename}")
            else:
                st.warning("No messages to export!")
    
    # Load saved chats
    saved_chats = get_saved_chats()
    if saved_chats:
        st.write("**Load saved chat:**")
        selected_chat = st.selectbox("Choose a saved chat:", [""] + saved_chats)
        if selected_chat:
            if st.button("📂 Load Chat", use_container_width=True):
                chat_data = load_chat_history(selected_chat)
                if chat_data:
                    st.session_state["messages"] = chat_data.get("messages", [])
                    if "model" in chat_data:
                        st.session_state["model"] = chat_data["model"]
                    if "system_prompt" in chat_data:
                        st.session_state["system_prompt"] = chat_data["system_prompt"]
                    st.success("Chat loaded successfully!")
                    st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    
    # Auto-save toggle
    st.session_state["auto_save"] = st.checkbox("Auto-save conversations", value=st.session_state["auto_save"])
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Statistics")
    st.metric("Messages in current chat", len(st.session_state["messages"]))
    st.metric("Saved chats", len(saved_chats))
    
    # GPU/CPU info
    if torch.cuda.is_available():
        st.success("🚀 GPU Available")
        st.info(f"Device: {torch.cuda.get_device_name()}")
    else:
        st.info("💻 Using CPU")

# Apply custom CSS
load_custom_css(st.session_state["theme_mode"])

# Main app
st.title("🦙 Enhanced Ollama Chatbot")

if st.session_state.get("system_prompt"):
    st.markdown(f"""
    <div class="system-prompt-box">
    <strong>🎯 System Prompt:</strong> {st.session_state["system_prompt"]}
    </div>
    """, unsafe_allow_html=True)

def model_res_generator():
    """Generate model response with system prompt support"""
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    
    # Prepare messages with system prompt if provided
    messages_with_system = []
    
    if st.session_state.get("system_prompt"):
        messages_with_system.append({
            "role": "system",
            "content": st.session_state["system_prompt"]
        })
    
    messages_with_system.extend(st.session_state["messages"])
    
    try:
        stream = ollama.chat(
            model=st.session_state["model"],
            messages=messages_with_system,
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except Exception as e:
        yield f"Error: {str(e)}"

# Display chat messages from history
for i, message in enumerate(st.session_state["messages"]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Enter your message here..."):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        if st.session_state.get("model"):
            try:
                message = st.write_stream(model_res_generator())
                st.session_state["messages"].append({"role": "assistant", "content": message})
                
                # Auto-save if enabled
                if st.session_state.get("auto_save") and len(st.session_state["messages"]) % 10 == 0:
                    save_chat_history(st.session_state["messages"])
                    
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        else:
            st.error("Please select a model first!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Enhanced Ollama Chatbot | Features: Chat History • System Prompts • Theme Toggle • Export
</div>
""", unsafe_allow_html=True)
