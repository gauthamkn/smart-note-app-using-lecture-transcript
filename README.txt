# 🧠 LLM Smart Notes Generator from Lectures

Turn your lecture **audio** or **text** into well-structured 📄 summaries, 📝 topic-wise notes, and 🎴 flashcards using Whisper & OpenAI GPT. Includes options to download as 📄 PDF and 🧾 Word documents!

---

## 🚀 Features

- 🎤 Transcribes audio files using Whisper
- 📄 Summarizes content using LLMs
- 📝 Generates topic-wise notes
- 🎴 Creates Q&A flashcards
- 💾 Download results as PDF or Word
- 🌙 Beautiful dark theme UI with responsive layout
- 🔐 Secure API key handling via `.env` file

---

## 📁 Supported Inputs

- Audio: .mp3, .wav, .m4a, .ogg
- Text: .txt

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

    git clone https://github.com/yourusername/llm-smart-notes.git
    cd llm-smart-notes

### 2. Create and Activate Virtual Environment (Optional)

    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows

### 3. Install Required Packages

    pip install -r requirements.txt

### 4. Setup `.env` File

Create a `.env` file in the root folder:

    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

> 🔐 Replace the value with your OpenAI API key. Make sure to keep this file private!

### 5. Run the App

    streamlit run app.py

---

## 🧠 Technologies Used

- 🧠 OpenAI GPT - Text summarization, notes, flashcards
- 🎤 Whisper - Audio-to-text transcription
- 🌐 Streamlit - Web UI
- 📦 Python - Backend logic
- 📄 python-docx & FPDF - Document export (Word & PDF)

---

## 📦 Folder Structure

    llm-smart-notes/
    ├── app.py
    ├── .env
    ├── requirements.txt
    ├── utils/
    │   ├── whisper_utils.py
    │   └── llm_utils.py
    ├── audio_uploads/
    └── outputs/

---

## 📝 Sample Output

- 📄 A concise summary
- 📝 Topic-wise notes
- 🎴 Q&A flashcards
- 🔽 Download buttons for PDF & Word

---

## 🤝 Contributing

Pull requests are welcome! Open issues to discuss suggestions or bugs.

---

## 🛡️ License

This project is licensed under the MIT License.

---

## 💬 Credits

Built with ❤️ using Streamlit, OpenAI GPT, and Whisper  
Made by Gautham

---

Attention:

add a .env with the api key for the generation of the notes..... :)


-------
## 🧪 Coming Soon

- 🧠 Note categorization by difficulty
- 🗣️ Multilingual audio support
- 🔗 Google Drive / Dropbox integration
