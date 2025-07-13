# EduPlannerBotAI

**EduPlannerBotAI** is a Telegram bot built with `aiogram 3.x` and powered by OpenAI GPT. It generates personalized study plans, exports them to PDF/TXT, and sends reminders as Telegram messages. All data is stored using TinyDB.

> **Note:** All code comments and docstrings are now in English for better international collaboration and code clarity.

## 📌 Features

- 📚 Generate personalized study plans (LLM/OpenAI, fallback to Groq)
- 📝 Export study plans to PDF/TXT
- ⏰ Send reminders as Telegram messages for each study step
- 🗄️ Store data using TinyDB
- 📊 Python 3.10–3.13 support

## 🆕 Groq Fallback Integration

If the OpenAI API is unavailable, out of quota, or not configured, the bot will automatically use [Groq](https://groq.com/) as a fallback LLM provider. Groq offers:

- **Fast and reliable generations**
- **No strict quotas for most users**
- **OpenAI-compatible API**
- **Always available fallback**

If both OpenAI and Groq are unavailable, the bot falls back to a local plan generator (simple stub).

### How it works

1. **Primary:** OpenAI API (if `OPENAI_API_KEY` is set and quota is available)
2. **Fallback:** [Groq](https://groq.com/) (if `GROQ_API_KEY` is set)
3. **Last resort:** Local plan generator (simple stub)

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

You can now choose your preferred language for all bot interactions! Use the `/language` command to select from English, Russian, or Spanish. The bot will automatically translate all responses, study plans, and reminders to your chosen language using LLMs (OpenAI or Groq). If translation is not possible, the original English text will be sent.

**Supported languages:**
- English (`en`)
- Русский (`ru`)
- Español (`es`)

Translations are performed in real time using the same LLMs that generate study plans, ensuring high-quality and context-aware results.

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

### 3. Create .env file
Create a `.env` file in the root directory or rename `.env.example` to `.env` and fill in your tokens:
```bash
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the bot
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

- 100% of core logic is covered by automated tests (`pytest`).
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
│   └── planner.py          # Study plan generation flow
├── services/               # Core logic and helper functions
│   ├── llm.py              # OpenAI and Groq integration
│   ├── pdf.py              # PDF export
│   ├── txt.py              # TXT export
│   ├── reminders.py        # Reminder simulation
│   └── db.py               # TinyDB database
├── .env                    # Environment variables
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

## 🛠 Technologies Used

| Component     | Purpose                                |
|---------------|----------------------------------------|
| Python 3.10+  | Programming language                   |
| aiogram 3.x   | Telegram Bot Framework                 |
| OpenAI API    | LLM for text generation                |
| Groq API      | Fallback LLM provider                  |
| fpdf          | PDF file generation                    |
| TinyDB        | Lightweight NoSQL database             |
| python-dotenv | Environment variable management        |
| aiofiles      | Asynchronous file operations           |

## 🔧 CI/CD

- GitHub Actions workflow for Pylint analysis and tests
- Python version compatibility: 3.10, 3.11, 3.12, 3.13
- Custom `.pylintrc` configuration

## 📝 Release 2.1.0 Highlights

- Full English codebase (comments, docstrings, messages)
- PEP8 and pylint compliance (score 10/10)
- Full test coverage for all services and handlers
- Improved error handling and async file operations
- Multilingual support with LLM-based translation
- Telegram reminders for study plans
- **Groq fallback LLM integration**
- **Arli AI fully removed**
- Ready for open source and team development

## 🆕 2025 Updates

- All messages and buttons always contain non-empty text, eliminating Telegram errors (Bad Request: text must be non-empty).
- Keyboards (format selection, next actions) are always accompanied by a short message to ensure buttons are displayed reliably.
- Language selection buttons are not translated, so the language filter works correctly.
- The entire bot scenario is fully localized: all messages, buttons, and files are translated to the user's selected language.
- The logic is maximally simplified, with no unnecessary conditions; all stages work reliably and predictably.
- Fallback to Groq is supported for generation and translation if OpenAI is unavailable.
- The project is ready for use and open for extension.

## ⚠️ Handling Frequent 429 Errors

If you're experiencing too many `429 Too Many Requests` errors, consider the following:

* ⏱ Increase `BASE_RETRY_DELAY`
* 🔁 Increase `MAX_RETRIES`
* 🧠 Use a lighter OpenAI model (e.g., `gpt-3.5-turbo` instead of `gpt-4`)
* 💳 Upgrade your OpenAI plan to one with a higher request quota

## 🤝 Collaboration

We welcome contributions! If you'd like to improve this bot:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push to your fork
5. Submit a pull request

## 📬 Contact
Created with ❤️. Feedback and collaboration:
[@Aleksandr_Tk](https://t.me/Aleksandr_Tk)

## 📄 License
MIT License