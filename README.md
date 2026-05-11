# NeuralCore AI — Studio Ghibli Drama Edition 🌿✨

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-Multimodal-orange.svg)
![Groq](https://img.shields.io/badge/Groq-Llama_3-black.svg)

**NeuralCore AI** is a highly advanced, multimodal Retrieval-Augmented Generation (RAG) application disguised as a magical, Studio Ghibli-inspired storytelling experience. 

Designed as a premium portfolio piece, this project bridges the gap between complex AI engineering (Vector Search, Video Processing, LLM-as-a-Judge) and immersive UI/UX design.

---

## 🌟 Key Features

### 1. Multimodal Document & Video Intelligence 🎥📄
- **PDF RAG:** Ingests large PDF documents using `PyPDFLoader`, chunks data, and stores it in a **FAISS Vector Database** using HuggingFace `all-MiniLM-L6-v2` embeddings.
- **Video Vision Engine:** Upload `.mp4` or `.mov` files. The system uses **OpenCV** to extract key frames and pipes them into **Google Gemini Flash** for deep multimodal video understanding.

### 2. The "Persona Engine" & Multilingual TTS 🗣️
- **Dynamic Roleplay:** Users select from three custom AI personas (Spirit of the Forest, Sky Navigator, Ancient Guardian). The system forces the LLM to strictly adhere to these dramatic personas via system prompting.
- **Neural TTS:** Generates high-quality, soothing, and melodious audio responses using **Microsoft Edge-TTS**. 
- **Multilingual Support:** Fully translates UI and enforces AI responses in English, Roman Urdu, and Native Urdu.

### 3. Dynamic Emotion UI (Watercolor Aesthetic) 🎨
- The entire Streamlit UI was overwritten with custom CSS to feature hand-painted watercolor textures, glassmorphism, and storybook typography (`Crimson Pro`).
- **Emotion Parsing:** The LLM is engineered to output hidden `[EMOTION]` tags (e.g., CALM, ACTION, DARK). The UI dynamically parses these tags and changes the CSS background color in real-time based on the sentiment of the story!

### 4. Enterprise-Grade Fallbacks & Automated Evaluation 📊
- **Local-to-Cloud Routing:** Intelligently routes queries to lightning-fast **Groq (Llama-3-70b)** APIs. If offline, it gracefully falls back to local inferencing via **Ollama (Llama-3.2)**.
- **LLM-as-a-Judge:** Includes a standalone `evaluate.py` script that uses a larger LLM to automatically score the RAG pipeline on "Accuracy" (Hallucination checks) and "Persona Adherence" out of 10.

---

## 🛠️ Technology Stack
- **Frontend:** Streamlit, Custom CSS (Glassmorphism, Dynamic Gradients)
- **Backend Core:** Python, LangChain, FAISS
- **LLM APIs:** Groq (Llama 3), Google Generative AI (Gemini Flash), Ollama (Local)
- **Audio & Video:** OpenCV (`cv2`), Edge-TTS (Microsoft Neural Voices)

---

## 🚀 Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/neuralcore-ghibli.git
   cd neuralcore-ghibli
   ```

2. **Set up a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_key_here
   GOOGLE_API_KEY=your_gemini_key_here
   ```

4. **Run the Application:**
   ```bash
   python -m streamlit run app.py
   ```

---

## 📈 Automated Evaluation (`evaluate.py`)
To test the hallucination rate and persona adherence of the RAG pipeline, run the automated LLM-as-a-Judge script:
```bash
python evaluate.py
```
*Outputs an accuracy and persona score out of 10 for enterprise QA validation.*


