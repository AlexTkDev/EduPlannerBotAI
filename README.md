# EduPlannerBotAI

**EduPlannerBotAI** is a Telegram bot built with `aiogram 3.x` and powered by a multi-level LLM architecture. It generates personalized study plans, exports them to PDF/TXT, and sends reminders as Telegram messages. All data is stored using TinyDB (no other DBs supported).

> **Note:** All code comments and docstrings are in English for international collaboration and code clarity. All user-facing messages and buttons are automatically translated to the user's selected language.

## 📌 Features

- 📚 Generate personalized study plans using multi-level LLM architecture
- 📝 Export study plans to PDF/TXT
- ⏰ Send reminders as Telegram messages for each study step
- 🗄️ Store data using TinyDB (no SQL/other DBs)
- 🌐 Multilingual: English, Russian, Spanish — all messages, buttons, and files are translated in real time using LLMs
- 🏷️ All keyboards are always shown with a short message, ensuring buttons are reliably displayed
- ❌ No empty or invisible messages — all user-facing text is always non-empty (prevents Telegram errors)
- 🔄 Language selection buttons are not translated, so the language filter works correctly
- 🤖 If translation is not possible, the original English text is sent
- 🧩 Simple, maintainable, idiomatic codebase — ready for extension
- 🚀 **NEW**: Local LLM integration for offline operation and guaranteed availability

## 🆕 Multi-Level LLM Architecture

The bot now features a sophisticated multi-level fallback system that ensures reliable service even when external APIs are unavailable:

### LLM Processing Chain

1. **OpenAI GPT** (Priority 1) - Primary model for generating study plans
2. **Groq** (Priority 2) - Secondary model, used if OpenAI is unavailable
3. **Local LLM** (Priority 3) - Local TinyLlama 1.1B model for offline operation
4. **Fallback Plan** (Priority 4) - Predefined high-quality study plan template

### How It Works

The bot automatically attempts to generate study plans using available services in order of priority:

1. **Primary**: OpenAI API (if `OPENAI_API_KEY` is set and quota is available)
2. **Fallback 1**: [Groq](https://groq.com/) (if `GROQ_API_KEY` is set)
3. **Fallback 2**: Local LLM (TinyLlama 1.1B model)
4. **Last Resort**: Local plan generator (comprehensive template)

### Local LLM Integration

The bot now includes a local TinyLlama 1.1B model that provides:

- **Offline Operation**: Works without internet connection
- **Fast Response**: No network latency
- **Privacy**: All processing happens locally
- **Guaranteed Availability**: Always accessible as fallback
- **High Quality**: Professional-grade study plan generation

### Translation Fallback

The same multi-level system applies to text translation:

1. **OpenAI** for high-quality translations
2. **Groq** as secondary translation service
3. **Local LLM** for offline translation capability
4. **Original Text** if all translation services fail

## 🆕 Groq Fallback Integration

If the OpenAI API is unavailable, out of quota, or not configured, the bot will automatically use [Groq](https://groq.com/) as a fallback LLM provider. Groq offers:

- **Fast and reliable generations**
- **No strict quotas for most users**
- **OpenAI-compatible API**
- **Always available fallback**

### How to use Groq

1. Register and get your API key at [Groq](https://console.groq.com/keys).
2. Add the following line to your `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```
3. (Optional) Add to `.env.example` for documentation:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

No other changes are needed — the bot will automatically use Groq if OpenAI is not available.

## 🌐 Multilingual Support

You can choose your preferred language for all bot interactions! Use the `/language` command to select from English, Russian, or Spanish. The bot will automatically translate all responses, study plans, and reminders to your chosen language using the multi-level LLM system.

**Supported languages:**
- English (`en`)
- Русский (`ru`)
- Español (`es`)

Translations are performed in real time using the same LLM architecture that generates study plans, ensuring high-quality and context-aware results. The system automatically falls back through available services to provide the best possible translation quality.

## 🚀 Quick Start

### 1. Clone the project
```bash
git clone https://github.com/AlexTkDev/EduPlannerBotAI.git
cd EduPlannerBotAI
```

### 2. Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up Local LLM (Optional but Recommended)
The bot includes a local TinyLlama 1.1B model for offline operation:

- **Model**: TinyLlama 1.1B Chat v1.0 (Q4_K_M quantized)
- **Format**: GGUF format
- **Size**: ~1.1GB
- **Requirements**: ~2GB RAM for optimal performance

The model is automatically loaded at startup and provides offline fallback capability.

### 4. Create .env file
Create a `.env` file in the root directory or rename `.env.example` to `.env` and fill in your tokens:
```bash
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```
All environment variables are loaded from `.env` automatically.

### 5. Run the bot
```bash
python bot.py
```

## 🐳 Run with Docker

You can run the bot in a container:
```bash
docker-compose up --build
```
Environment variables are loaded from `.env`.

## 🔔 How Reminders Work

When you choose to schedule reminders, the bot will send you a separate Telegram message for each step of your study plan. This ensures you receive timely notifications directly in your chat.

## 🧪 Testing & Code Quality

- 100% of core logic and all handlers are covered by automated tests (`pytest`).
- Code style: PEP8, pylint score 10/10 (see `.pylintrc`).
- To run tests:
  ```bash
  pytest
  ```

## ⚙️ Project Structure
```
EduPlannerBotAI/
├── bot.py                  # Bot entry point
├── config.py               # Load tokens from .env
├── handlers/               # Command and message handlers
│   ├── __init__.py
│   ├── start.py            # /start and greeting
│   ├── planner.py          # Study plan generation flow
│   └── language.py         # Language selection and filter
├── services/               # Core logic and helper functions
│   ├── llm.py              # Multi-level LLM integration (OpenAI → Groq → Local LLM → Fallback)
│   ├── local_llm.py        # Local TinyLlama model integration
│   ├── pdf.py              # PDF export
│   ├── txt.py              # TXT export
│   ├── reminders.py        # Reminder simulation
│   └── db.py               # TinyDB database
├── models/                  # Local LLM model storage
│   └── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
├── .env                    # Environment variables
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

## 🛠 Technologies Used

| Component     | Purpose                                |
|---------------|----------------------------------------|
| Python 3.10+  | Programming language                   |
| aiogram 3.x   | Telegram Bot Framework                 |
| OpenAI API    | Primary LLM for text generation and translation|
| Groq API      | Secondary LLM provider (generation+translation) |
| Local LLM     | TinyLlama 1.1B for offline operation  |
| llama-cpp-python | Local LLM inference engine           |
| fpdf          | PDF file generation                    |
| TinyDB        | Lightweight NoSQL database             |
| python-dotenv | Environment variable management        |
| aiofiles      | Asynchronous file operations           |

## 🔧 CI/CD

- GitHub Actions workflow for Pylint analysis and tests
- Python version compatibility: 3.10, 3.11, 3.12, 3.13
- Custom `.pylintrc` configuration

## 📝 Release 4.0.0 Highlights

- **Multi-Level LLM Architecture**: OpenAI → Groq → Local LLM → Fallback Plan
- **Local LLM Integration**: TinyLlama 1.1B model for offline operation
- **Guaranteed Availability**: Bot works even without internet connection
- **Enhanced Fallback System**: Robust error handling and service switching
- **Improved Plan Quality**: Professional-grade study plan templates
- **Offline Translation**: Local LLM supports offline text translation
- **Performance Optimization**: Efficient model loading and inference
- **Comprehensive Logging**: Detailed monitoring of LLM service transitions
- All user-facing messages and buttons always contain non-empty text, eliminating Telegram errors
- The entire bot scenario is fully localized with multi-level translation fallback
- Codebase is fully in English (comments, docstrings, messages), PEP8 and pylint compliant
- 100% test coverage for all core logic and handlers
- Project is ready for production use and easy extension

## ⚠️ Handling Frequent 429 Errors

If you're experiencing too many `429 Too Many Requests` errors, consider the following:

* ⏱ Increase `BASE_RETRY_DELAY`
* 🔁 Increase `MAX_RETRIES`
* 🧠 Use a lighter OpenAI model (e.g., `gpt-3.5-turbo` instead of `gpt-4`)
* 💳 Upgrade your OpenAI plan to one with a higher request quota
* 🚀 **NEW**: The bot will automatically fall back to Groq and Local LLM to maintain service availability

## 🤝 Collaboration

We welcome contributions! If you'd like to improve this bot:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (all code and comments must be in English)
4. Push to your fork
5. Submit a pull request

## 📬 Contact
Created with ❤️. Feedback and collaboration:
[@Aleksandr_Tk](https://t.me/Aleksandr_Tk)

## 📄 License
MIT License