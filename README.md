# EduPlannerBotAI

**EduPlannerBotAI** is a Telegram bot built with `aiogram 3.x` and powered by OpenAI GPT. It generates personalized study plans, exports them to PDF/TXT, and sends reminders as Telegram messages. All data is stored using TinyDB.

> **Note:** All code comments and docstrings are now in English for better international collaboration and code clarity.

## 📌 Features

- 📚 Generate personalized study plans (LLM/OpenAI)
- 📝 Export study plans to PDF/TXT
- ⏰ Send reminders as Telegram messages for each study step
- 🗄️ Store data using TinyDB
- 📊 Python 3.10–3.13 support

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
│   ├── llm.py              # OpenAI integration
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
| fpdf          | PDF file generation                    |
| TinyDB        | Lightweight NoSQL database             |
| python-dotenv | Environment variable management        |
| aiofiles      | Asynchronous file operations           |

## 🔧 CI/CD

- GitHub Actions workflow for Pylint analysis and tests
- Python version compatibility: 3.10, 3.11, 3.12, 3.13
- Custom `.pylintrc` configuration

## 📝 Release 2.0.0 Highlights

- Full English codebase (comments, docstrings, messages)
- PEP8 and pylint compliance (score 10/10)
- Full test coverage for all services and handlers
- Improved error handling and async file operations
- Ready for open source and team development

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