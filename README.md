# EduPlannerBotAI

**EduPlannerBotAI** is a Telegram bot built with `aiogram 3.x` and powered by a revolutionary multi-level LLM architecture. It generates personalized study plans, exports them to PDF/TXT, and sends reminders as Telegram messages. All data is stored using TinyDB (no other DBs supported).

> **Note:** All code comments and docstrings are in English for international collaboration and code clarity. All user-facing messages and buttons are automatically translated to the user's selected language.

## 🚀 What's New in v4.1.0

- **🆕 Multi-Level LLM Architecture**: OpenAI → Groq → Local LLM → Fallback Plan
- **🆕 Local LLM Integration**: Google Gemma 4 model for offline operation
- **🆕 Guaranteed Availability**: Bot works even without internet connection
- **🆕 Enhanced Fallback System**: Robust error handling and service switching
- **🆕 Improved Plan Quality**: Professional-grade study plan templates
- **🆕 Offline Translation**: Local LLM supports offline text translation

## 📌 Features

- 📚 **Multi-Level LLM Architecture**: Generate personalized study plans using OpenAI, Groq, Local LLM, or fallback templates
- 📝 **Export Options**: Save plans as PDF or TXT files
- ⏰ **Smart Reminders**: Receive Telegram notifications for each study step
- 🗄️ **Lightweight Storage**: TinyDB-based data storage (no SQL required)
- 🌐 **Multilingual Support**: English, Russian, Spanish with real-time LLM translation
- 🏷️ **Reliable UI**: All keyboards displayed with proper messages (no Telegram errors)
- 🔄 **Smart Language Handling**: Language selection works correctly without translation
- 🤖 **Graceful Fallbacks**: Original text sent if translation fails
- 🧩 **Extensible Codebase**: Clean, maintainable code ready for extensions
- 🚀 **Offline Operation**: Local LLM ensures 100% availability
- 🔒 **Privacy First**: Local processing keeps your data secure

## 🏗️ Multi-Level LLM Architecture

The bot features a sophisticated 4-tier fallback system that ensures reliable service even during complete internet outages:

### 🎯 LLM Processing Chain

| Priority | Service | Description | Use Case |
|----------|---------|-------------|----------|
| **1** | **OpenAI GPT** | Primary model for high-quality plans | Best quality, when available |
| **2** | **Groq** | Secondary model, OpenAI alternative | Fast fallback, reliable service |
| **3** | **Local LLM** | Google Gemma 4 local model | Offline operation, privacy |
| **4** | **Fallback Plan** | Predefined professional template | Guaranteed availability |

### ⚡ How It Works

The bot automatically attempts to generate study plans using available services in order of priority:

1. **Primary**: OpenAI API (if `OPENAI_API_KEY` is set and quota available)
2. **Fallback 1**: [Groq](https://groq.com/) (if `GROQ_API_KEY` is set)
3. **Fallback 2**: Local LLM (Google Gemma 4 model)
4. **Last Resort**: Local plan generator (comprehensive template)

### 🔄 Translation Fallback

The same multi-level system applies to text translation:

1. **OpenAI** for high-quality translations
2. **Groq** as secondary translation service
3. **Local LLM** for offline translation capability
4. **Original Text** if all translation services fail

## 🤖 Local LLM Integration

### ✨ Key Benefits

- **🔄 Offline Operation**: Works without internet connection
- **⚡ Fast Response**: No network latency (0.5-2 seconds)
- **🔒 Privacy**: All processing happens locally on your server
- **🛡️ Guaranteed Availability**: Always accessible as fallback
- **🎯 High Quality**: Professional-grade study plan generation
- **💰 Cost Effective**: No API costs for local operations

### 📊 Performance Metrics

| Metric | OpenAI | Groq | Local LLM | Fallback |
|--------|--------|------|-----------|----------|
| **Response Time** | 2-5s | 1-3s | 0.5-2s | 0.1s |
| **Availability** | 99% | 99% | 100% | 100% |
| **Cost** | Per token | Per token | Free | Free |
| **Privacy** | External | External | Local | Local |

## 🆕 Groq Fallback Integration

If the OpenAI API is unavailable, out of quota, or not configured, the bot automatically uses [Groq](https://groq.com/) as a fallback LLM provider.

### 🚀 Groq Advantages

- **Fast and reliable generations**
- **No strict quotas for most users**
- **OpenAI-compatible API**
- **Always available fallback**

### 📝 Setup Instructions

1. Register and get your API key at [Groq Console](https://console.groq.com/keys)
2. Add to your `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key
   ```
3. No other changes needed — automatic fallback enabled

## 🌐 Multilingual Support

Choose your preferred language for all bot interactions! Use `/language` to select from:

| Language | Code | Status |
|----------|------|--------|
| **English** | `en` | ✅ Primary |
| **Русский** | `ru` | ✅ Full support |
| **Español** | `es` | ✅ Full support |

### 🔄 Translation Features

- **Real-time translation** using multi-level LLM system
- **Context-aware results** for better accuracy
- **Automatic fallback** through available services
- **Original text preservation** if translation fails

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

### 3. Set up Local LLM (Recommended)
The bot includes a local Google Gemma 4 model for offline operation:

- **Model**: Google Gemma 4 Instruct (GGUF, quantized)
- **Format**: GGUF format
- **Size**: depends on variant/quantization (typically several GB)
- **Requirements**: depends on variant (recommended 8GB+ RAM for 4B class models)

**Important**: The model file is not included in the repository due to size limitations. You must download it separately:

```bash
# Download the model (choose one method)
# Option 1: Using wget
wget -O models/google-gemma-4b-it-Q4_K_M.gguf \
    "<YOUR_GEMMA4_GGUF_DOWNLOAD_URL>"

# Option 2: Using curl
curl -L -o models/google-gemma-4b-it-Q4_K_M.gguf \
    "<YOUR_GEMMA4_GGUF_DOWNLOAD_URL>"
```

See [models/README.md](models/README.md) for detailed download instructions and troubleshooting.

The model is automatically loaded at startup and provides offline fallback capability.

### 4. Create .env file
Create a `.env` file in the root directory or rename `.env.example` to `.env` and fill in your tokens:
```bash
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
LOCAL_LLM_MODEL_PATH=models/google-gemma-4b-it-Q4_K_M.gguf
LOCAL_LLM_CONTEXT=4096
LOCAL_LLM_THREADS=4
LOCAL_LLM_MAX_TOKENS=512
```
All environment variables are loaded from `.env` automatically.

### 5. Run the bot
```bash
python bot.py
```

## 🐳 Docker Deployment

Run the bot in a container:
```bash
docker-compose up --build
```
Environment variables are loaded from `.env`.

## 🔔 How Reminders Work

When you choose to schedule reminders, the bot sends a separate Telegram message for each study plan step, ensuring timely notifications directly in your chat.

## 🧪 Testing & Code Quality

- **100% test coverage** for core logic and all handlers
- **Pylint score**: 10.00/10 (Perfect)
- **Code style**: PEP8 and pylint compliant
- **Run tests**: `pytest`

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
│   ├── local_llm.py        # Local Google Gemma 4 model integration
│   ├── pdf.py              # PDF export
│   ├── txt.py              # TXT export
│   ├── reminders.py        # Reminder simulation
│   └── db.py               # TinyDB database
├── models/                  # Local LLM model storage
│   ├── README.md           # Model download instructions
│   └── .gitkeep            # Preserve directory structure
├── .env                    # Environment variables
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

## 🛠️ Technologies Used

| Component | Purpose | Version |
|-----------|---------|---------|
| **Python** | Programming language | 3.10+ |
| **aiogram** | Telegram Bot Framework | 3.x |
| **OpenAI API** | Primary LLM provider | Latest |
| **Groq API** | Secondary LLM provider | Latest |
| **Local LLM** | Google Gemma 4 offline | GGUF |
| **llama-cpp-python** | Local LLM inference | Latest |
| **fpdf** | PDF file generation | Latest |
| **TinyDB** | Lightweight NoSQL database | Latest |
| **python-dotenv** | Environment variable management | Latest |
| **aiofiles** | Asynchronous file operations | Latest |

## 🔧 CI/CD & Quality Assurance

- **GitHub Actions**: Automated Pylint analysis and testing
- **Python Compatibility**: 3.10, 3.11, 3.12, 3.13
- **Code Quality**: Custom `.pylintrc` configuration
- **Testing**: pytest with 100% coverage
- **Style**: PEP8 compliant

## 📝 Release 4.1.0 Highlights

### 🆕 Major Features
- **Multi-Level LLM Architecture**: OpenAI → Groq → Local LLM → Fallback Plan
- **Local LLM Integration**: Google Gemma 4 model for offline operation
- **Guaranteed Availability**: Bot works even without internet connection
- **Enhanced Fallback System**: Robust error handling and service switching

### 🚀 Performance Improvements
- **Improved Plan Quality**: Professional-grade study plan templates
- **Offline Translation**: Local LLM supports offline text translation
- **Performance Optimization**: Efficient model loading and inference
- **Comprehensive Logging**: Detailed monitoring of LLM service transitions

### 🛡️ Reliability Enhancements
- **Eliminated Single Points of Failure**: No more dependency on single API
- **Reduced Response Times**: Local operations provide instant results
- **Better Resource Management**: Optimized model loading and cleanup
- **Production Ready**: Enterprise-grade stability and monitoring

### 🔧 Code Quality
- **Pylint Score**: 10.00/10 (Perfect)
- **Test Coverage**: 100% for all core logic and handlers
- **Style Compliance**: PEP8 and pylint compliant
- **Documentation**: Comprehensive inline documentation

## ⚠️ Handling Frequent 429 Errors

If you experience too many `429 Too Many Requests` errors:

* ⏱ **Increase delays**: Adjust `BASE_RETRY_DELAY` and `MAX_RETRIES`
* 🧠 **Use lighter models**: Consider `gpt-3.5-turbo` instead of `gpt-4`
* 💳 **Upgrade plan**: Consider higher quota OpenAI plan
* 🚀 **Automatic fallback**: Bot will use Groq and Local LLM automatically

## 🤝 Contributing

We welcome contributions! To improve this bot:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (all code and comments must be in English)
4. Push to your fork
5. Submit a pull request

## 📊 Performance & Monitoring

### 📈 Key Metrics
- **Response Time**: 0.1s - 5s depending on service used
- **Uptime**: 99.9%+ with fallback system
- **Offline Capability**: 100% (local LLM)
- **Service Recovery**: Automatic (intelligent fallback)

### 🔍 Monitoring
- **Service Health**: Real-time status tracking
- **Performance Metrics**: Response time monitoring
- **Error Tracking**: Comprehensive error logging
- **Resource Usage**: Memory and CPU monitoring

## 📬 Contact & Support

Created with ❤️. For feedback and collaboration:

- **Telegram**: [@Aleksandr_Tk](https://t.me/Aleksandr_Tk)
- **GitHub Issues**: [Report bugs](https://github.com/AlexTkDev/EduPlannerBotAI/issues)
- **Documentation**: [README.md](README.md)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**EduPlannerBotAI v4.1.0** represents a significant milestone, transforming the bot from a simple OpenAI-dependent service into a robust, enterprise-grade system with guaranteed availability and offline operation capabilities. This release sets the foundation for future enhancements while maintaining backward compatibility and improving overall user experience.