# 🦙 Enhanced Ollama Chatbot

A feature-rich Streamlit webapp UI for local LLM implementation on Ollama. This enhanced version includes chat history persistence, system prompts, dark/light mode toggle, and much more!

With just a few Python libraries, you can have a powerful, localized LLM chat interface with professional features.

## ✨ New Features

### 🎨 **Dark/Light Theme Toggle**
- Beautiful dark and light mode themes
- Custom CSS styling for better user experience
- Seamless theme switching

### 💾 **Chat History Management**
- **Auto-save**: Automatically saves conversations every 10 messages
- **Manual save**: Save conversations anytime with custom names
- **Load chats**: Resume previous conversations
- **Export to Markdown**: Download conversations as formatted .md files
- **Statistics**: Track your chat metrics

### ⚙️ **System Prompt Customization**
- **Preset prompts**: Choose from helpful presets like:
  - Helpful Assistant
  - Code Assistant 
  - Creative Writer
  - Teacher
  - Pirate 🏴‍☠️
  - Philosopher
- **Custom prompts**: Write your own system prompts
- **Live preview**: See active system prompt in the chat

### 🚀 **Enhanced UI/UX**
- **Sidebar organization**: Clean, organized controls
- **GPU/CPU detection**: Shows hardware status
- **Message statistics**: Track conversation length
- **Error handling**: Better error messages and recovery
- **Professional styling**: Modern, polished interface

## 🎯 Recommended Models

**For coding:** `codellama`, `dolphin-mixtral`, `deepseek-coder`  
**For everyday questions:** `mixtral`, `mistral`, `llama2`  
**For creative tasks:** `llama2`, `mixtral`

Full model library: https://ollama.com/library

## 🚀 Quick Start

### Prerequisites
- Ollama installed and running
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/romilandc/streamlit-ollama-llm.git
   cd streamlit-ollama-llm
   ```

2. **Create virtual environment**
   ```bash
   # Using conda
   conda create -n ollama python=3.9
   conda activate ollama
   
   # Or using venv
   python -m venv ollama
   source ollama/bin/activate  # Linux/Mac
   # ollama\Scripts\activate     # Windows
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama** (if not already running)
   ```bash
   ollama serve
   ```

5. **Download models** (if you haven't already)
   ```bash
   ollama pull llama2        # Basic model
   ollama pull codellama     # For coding
   ollama pull mixtral       # More advanced
   ```

6. **Run the app**
   ```bash
   streamlit run llm_app.py
   ```

7. **Open your browser**
   - Navigate to the URL shown in terminal (usually `http://localhost:8501`)
   - Select your model and start chatting!

## 📖 Usage Guide

### Basic Chat
1. Select your preferred model from the dropdown
2. Optionally set a system prompt for specific behavior
3. Type your message and press Enter
4. Enjoy conversing with your local LLM!

### System Prompts
- Choose from preset prompts or create custom ones
- System prompts guide the AI's personality and behavior
- Great for specialized tasks (coding, writing, teaching, etc.)

### Chat History
- **Auto-save**: Enabled by default, saves every 10 messages
- **Manual save**: Click "💾 Save Chat" to save anytime
- **Load previous chats**: Select from saved conversations
- **Export**: Download as markdown for external use

### Theme Customization
- Toggle between Light and Dark modes
- Theme persists across sessions
- Optimized for readability in both modes

## 🔧 Configuration

### Chat History Location
- Saved in `chat_history/` directory
- JSON format for chats, Markdown for exports
- Includes timestamps, model info, and system prompts

### Auto-save Settings
- Saves every 10 messages by default
- Can be toggled on/off in sidebar
- Includes full conversation context

## 🎨 Screenshots

### Light Mode
![Light Mode Interface](img/light_mode_example.png)

### Dark Mode  
![Dark Mode Interface](img/dark_mode_example.png)

### System Prompt Configuration
![System Prompts](img/system_prompts_example.png)

### Chat History Management
![Chat History](img/chat_history_example.png)

## 🛠️ Technical Details

### Hardware Requirements
- **Minimum**: 4GB RAM (for small models like Phi-2)
- **Recommended**: 8GB+ RAM, GPU for larger models
- **Storage**: 2GB+ for model storage

### GPU Support
- Automatically detects CUDA availability
- Falls back to CPU if no GPU present
- Shows hardware status in sidebar

### File Structure
```
streamlit-ollama-llm/
├── llm_app.py              # Main application
├── requirements.txt        # Dependencies
├── README.md              # This file
├── chat_history/          # Saved conversations (auto-created)
│   ├── chat_*.json       # JSON chat files
│   └── chat_export_*.md  # Markdown exports
└── img/                   # Screenshots
```

## 🤝 Contributing

We welcome contributions! Some ideas for future enhancements:

- **Multi-model comparison**: Chat with multiple models simultaneously
- **Voice input/output**: Speech-to-text and text-to-speech
- **File upload support**: Chat about documents and images
- **Advanced model parameters**: Temperature, top-k, top-p controls
- **Conversation search**: Find specific messages in history
- **Chat templates**: Pre-built conversation starters
- **API integrations**: Connect to external services

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**"No Ollama models found"**
- Make sure Ollama is running: `ollama serve`
- Install models: `ollama pull llama2`
- Check Ollama status: `ollama list`

**"Error connecting to Ollama"**
- Verify Ollama is running on localhost:11434
- Try restarting Ollama service
- Check firewall settings

**App won't start**
- Update Streamlit: `pip install --upgrade streamlit`
- Check Python version (3.8+ required)
- Install missing dependencies: `pip install -r requirements.txt`

**Chat history not saving**
- Check write permissions in directory
- Ensure `chat_history/` folder exists
- Look for error messages in sidebar

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original project by [romilandc](https://github.com/romilandc)
- Built with [Streamlit](https://streamlit.io/)
- Powered by [Ollama](https://ollama.ai/)
- Enhanced with ❤️ by the community

## 🔗 Links

- **Ollama**: https://ollama.ai/
- **Streamlit**: https://streamlit.io/
- **Model Library**: https://ollama.ai/library
- **Original Repository**: https://github.com/romilandc/streamlit-ollama-llm

---

**Enjoy your enhanced local LLM experience! 🚀**

*If you find this useful, please consider giving it a ⭐ and sharing with others!*
