# Snap-Study
# 📚 Snap & Study

### Snap it. Understand it. Save it for later.

Snap & Study is an AI-powered educational chatbot that helps students understand difficult academic concepts using images and text. Students can upload photos of textbook pages, handwritten notes, diagrams, or mathematical problems and receive simple explanations and step-by-step solutions using Google's Gemini AI.

Students can also generate a study summary from their conversation and send it to WhatsApp for future revision.

## ✨ Features

- 📸 **AI Vision:** Upload images of questions, diagrams, textbook pages, and handwritten notes.
- 🧠 **Smart Explanations:** Understand difficult concepts in simple, student-friendly language.
- 📝 **Step-by-Step Solutions:** Get logical explanations for mathematical and scientific problems.
- 💬 **Interactive Chatbot:** Ask follow-up questions and clarify doubts.
- 📚 **Study Summaries:** Summarize key concepts, definitions, formulas, and examples from conversations.
- 📲 **WhatsApp Sharing:** Send study summaries to your WhatsApp number.
- 🎓 **Multiple Subjects:** Get help with mathematics, physics, chemistry, biology, computer science, programming, and more.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web application interface |
| Google Gemini API | AI-powered image understanding and explanations |
| Google Gen AI SDK | Communication with Gemini |
| Twilio API | WhatsApp message delivery |
| Git & GitHub | Version control and source code hosting |

## ⚙️ How It Works

1. **Get Started:** Enter your name and WhatsApp number.
2. **Upload or Ask:** Submit a photo of a question or type your doubt.
3. **Understand:** Gemini analyzes the content and generates an explanation.
4. **Explore:** Ask follow-up questions to understand the concept better.
5. **Save:** Request a study summary and send it to WhatsApp.

## 📂 Project Structure

```text
Snap-Study/
├── app.py                  # Main Streamlit application
├── prompts.py              # AI system, welcome, and summary prompts
├── .gitignore              # Excludes secrets and unnecessary files
├── requirements.txt         # Python dependencies
└── .streamlit/
    └── secrets.toml         # Local API credentials (never commit)
```

The `.streamlit/secrets.toml` file is a local configuration file and should not be uploaded to GitHub.

## 🚀 Getting Started

### Prerequisites

Before running the project, install:

- Python 3.10 or a compatible version supported by your dependencies
- Git
- A Google Gemini API key
- A Twilio account configured for WhatsApp messaging

### 1. Clone the repository

```bash
git clone https://github.com/Manoj07-igris/Snap-Study.git
cd Snap-Study
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt and run:

```bat
venv\Scripts\activate.bat
```

### 3. Install dependencies

If `requirements.txt` exists:

```bash
python -m pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
python -m pip install streamlit google-genai twilio
```

### 4. Configure API credentials

Create a folder named `.streamlit` in your project directory if it does not already exist.

Inside it, create `secrets.toml` and add your credentials:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_WHATSAPP_FROM = "whatsapp:+your-twilio-number"
TWILIO_CONTENT_SID = "your-approved-template-sid"
```

Replace the placeholder values with your actual credentials.

**Security:** Never share your API keys, authentication tokens, or `secrets.toml` file publicly. Keep this file excluded through `.gitignore`.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in your terminal. Open it in your browser to use Snap & Study.

## 🔑 API Setup

### Google Gemini

1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Obtain a Gemini API key.
3. Add it to your local `secrets.toml` file.
4. Configure `MODEL_NAME` in `app.py` to use a currently supported vision-capable Gemini model available to your account.

### Twilio WhatsApp

1. Create an account at [Twilio](https://www.twilio.com/).
2. Configure WhatsApp messaging through Twilio.
3. Set up an appropriate WhatsApp content template with student-name and study-summary placeholders.
4. Add the corresponding credentials and template SID to `secrets.toml`.

WhatsApp delivery depends on valid Twilio configuration, applicable messaging rules, and recipient eligibility.

## 🔒 Security and Privacy

- API credentials should be stored in Streamlit secrets, not hardcoded in source files.
- Do not commit `.streamlit/secrets.toml` or `.env` files.
- Uploaded images are sent to the configured AI service for processing.
- Review the privacy policies of the services used before uploading sensitive educational material.

## 🔮 Future Enhancements

- 📩 Email sharing for study summaries.
- ✈️ Telegram sharing integration.
- 🗣️ Voice-based questions and explanations.
- 🌐 Support for multiple languages.
- 🧪 Interactive quizzes and practice questions.
- 📖 Saved notes and searchable study history.
- 🎨 Interactive visual explanations of complex concepts.

These are planned enhancements and may not be available in the current version.

## 🎯 Project Goal

Snap & Study aims to make learning easier and more accessible by turning confusing educational content into understandable explanations. It helps students move beyond memorizing answers toward understanding the concepts behind them.

## 👨‍💻 Author

**Manojkumar**

GitHub: [@Manoj07-igris](https://github.com/Manoj07-igris)

## 📄 License

No license has been specified yet. If you plan to make this project open source, consider adding an appropriate license file.

---

**Snap & Study — Learn smarter, one snap at a time! 📚🚀**
