# EduPlannerBotAI

**EduPlannerBotAI** is a Telegram bot built with `aiogram 3.x` and powered by OpenAI GPT. It generates personalized study plans, exports them to PDF, visualizes them as charts, and schedules reminders. All data is stored using TinyDB.

---

## 📌 Features

- 📚 Generate personalized study plans (LLM/OpenAI)
- 📝 Export study plans to PDF
- 📊 Visualize plans with charts (matplotlib)
- ⏰ Schedule reminders (async simulation)
- 🗄️ Store data using TinyDB

---

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
pip install -r requirements.txt.py
```

### 3. Create .env file
Create a `.env` file in the root directory:
```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the bot
```bash
python bot.py
```

---

## ⚙️ Project Structure
```
EduPlannerBotAI/
├── bot.py                  # Bot entry point
├── config.py               # Load tokens from .env
├── handlers/               # Command and message handlers
│   ├── __init__.py
│   ├── start.py            # /start and greeting
│   └── planner.py          # Handle user requests
├── services/               # Core logic and helper functions
│   ├── llm.py              # OpenAI integration
│   ├── pdf.py              # PDF export
│   ├── chart.py            # Chart generation
│   ├── reminders.py        # Reminder simulation
│   └── db.py               # TinyDB database
├── .env                    # Environment variables
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

---

## 🛠 Technologies Used

| Component         | Purpose                                |
|------------------|----------------------------------------|
| Python 3.11+      | Programming language                   |
| aiogram 3.x       | Telegram Bot Framework                 |
| OpenAI API        | LLM for text generation                |
| matplotlib        | Chart rendering                        |
| fpdf              | PDF file generation                    |
| TinyDB            | Lightweight NoSQL database             |
| python-dotenv     | Environment variable management        |

---

## 🤝 Collaboration

We welcome contributions! If you'd like to improve this bot, fix bugs, or add features:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push to your fork
5. Submit a pull request

---

## 📬 Contact
Created with ❤️ for educational purposes. Feedback and collaboration:
[@Aleksandr_Tk](https://t.me/Aleksandr_Tk)

---

## 📄 License
MIT License
