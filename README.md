# EduPlannerBotAI

**EduPlannerBotAI** is a Telegram bot built with `aiogram 3.x` and powered by OpenAI GPT. It generates personalized study plans, exports them to PDF/TXT, and schedules reminders. All data is stored using TinyDB.

## 📌 Features

- 📚 Generate personalized study plans (LLM/OpenAI)
- 📝 Export study plans to PDF/TXT
- ⏰ Schedule reminders (async simulation)
- 🗄️ Store data using TinyDB

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

## 🔧 CI/CD

- GitHub Actions workflow for Pylint analysis
- Python version compatibility: 3.10, 3.11, 3.12, 3.13
- Custom `.pylintrc` configuration

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