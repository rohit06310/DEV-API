# ⚡ DevFlow — API Integration Accelerator

DevFlow is an AI-powered, interactive web application built on **Streamlit** and the **Groq LLaMA 3.3** model. It helps developers, researchers, and students understand, test, and integrate REST APIs in under 60 seconds. Given any API documentation URL, DevFlow automatically parses it, extracts structured metadata, provides a live HTTP testing sandbox, and generates production-ready client SDKs in 6 programming languages.

---

## 🚀 Key Features

*   **🔍 Smart AI Documentation Parsing**: Instantly extracts API name, version, base URL, auth schemas, rate limits, and endpoints from raw documentation web pages using LLaMA 3.3.
*   **🔗 Interactive Endpoint Explorer**: Easily browse, search, and filter extracted endpoints (GET, POST, PUT, DELETE, PATCH) with dynamic method badges and description details. Export the full endpoint manifest as CSV.
*   **🔐 Auth Guide & Code Snippets**: Automatically isolates authentication headers, generating copy-paste ready reference code for cURL, Python (requests), and JavaScript (fetch).
*   **⚙️ Multi-Language SDK Generator**: Generates custom helper functions or complete object-oriented wrapper classes (fully documented with type hinting and exception handling) for:
    *   *Python, JavaScript, TypeScript, Java, Go, cURL*
*   **🧪 Live HTTP Sandbox**: Test requests directly from the interface. Includes JSON payload validation, root URL warnings, latency metrics, header viewers, and a request history log.
*   **🐙 Built-in Preset APIs**: Jump straight in with one-click presets for popular APIs including GitHub, Stripe, Twilio, Razorpay, OpenWeatherMap, and Alpha Vantage.

---

## 🛠️ Technology Stack

*   **Frontend & UI**: Streamlit (with customized CSS/Glassmorphism styling)
*   **AI Backend**: Groq Inference API (`llama-3.3-70b-versatile`, fallback: `llama3-8b-8192`)
*   **Data Wrangling**: Pandas, BeautifulSoup4, lxml
*   **HTTP Client**: Requests

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/rohit06310/DEV-API.git
cd DEV-API
```

### 2. Configure Your Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> 💡 *Get a free Groq API key by signing up at the [Groq Console](https://console.groq.com).*

---

## 🚀 Running the App Locally

To start the DevFlow server, run:
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## 📦 Deployment

DevFlow is ready for deployment on **Streamlit Community Cloud**:
1. Push your repository to GitHub (already set up).
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud).
3. Specify `app.py` as the entry point and add your `GROQ_API_KEY` under the app's **Advanced Settings / Secrets** (do NOT commit your `.env` file).

---

## 📄 License
This project is licensed under the ISC License.
