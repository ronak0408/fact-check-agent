# 🔍 Fact-Check AI Agent

A Web application that automatically extracts and verifies factual claims from uploaded PDF documents using LLMs and live web search.

Built as a technical assessment project focused on combating hallucinated or outdated information in marketing and business documents.

---

## 🚀 Features

### 📄 PDF Upload & Parsing
- Upload PDF documents directly through the Streamlit frontend
- Extracts text using PyMuPDF

### 🧠 Claim Extraction
- Automatically detects factual claims from PDFs
- Supports:
  - statistics
  - dates
  - scientific statements
  - technical claims
  - financial claims

### 🌐 Live Web Verification
- Uses Tavily Search API for real-time evidence gathering
- Cross-checks claims against live web data

### ✅ Intelligent Verdict System
Each claim is classified as:
- VERIFIED
- INACCURATE
- FALSE

### 📊 Detailed Verification Reports
For every claim, the app provides:
- verdict
- explanation
- corrected fact
- confidence score
- source links

### 🎨 Modern UI
- Dark-themed professional interface
- Expandable verification cards
- Multi-claim support

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM Provider | OpenRouter |
| LLM Model | Llama 3.1 8B Instruct |
| Web Search | Tavily API |
| PDF Parsing | PyMuPDF |
| Backend | Python |

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ronak0408/fact-check-agent.git
cd fact-check-agent
```

---

### 2️⃣ Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root folder:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

### 5️⃣ Run Application

```bash
streamlit run app.py
```

---

## 🔑 API Keys

### OpenRouter
Get API key from:

https://openrouter.ai

### Tavily
Get API key from:

https://tavily.com

---

## 📸 Demo Workflow

1. Upload PDF
2. Extract claims automatically
3. Verify claims using live web search
4. Generate verification report

---

## 📌 Example Claims Tested

### VERIFIED
- The Earth revolves around the Sun.

### INACCURATE
- OpenAI was founded in 2018.

### FALSE
- Pluto is classified as the ninth planet of the Solar System.

---

## 👨‍💻 Author

Ronak Sain
