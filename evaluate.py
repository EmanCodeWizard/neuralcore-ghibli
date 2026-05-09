import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# ── Load Environment Variables ──
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY not found in .env file.")
    exit(1)

# Initialize the Judge LLM
judge_llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile", temperature=0.0)

# ── 1. Define Dummy Ground Truth Dataset ──
dataset = [
    {
        "id": 1,
        "context": "The company refund policy states that items can be returned within 30 days of purchase with a valid receipt. Digital items are strictly non-refundable.",
        "question": "Can I return a video game I downloaded yesterday?",
        "generated_answer": "*[The Spirit of the Forest rustles the leaves sadly...]* Ah, little traveler, the laws of this realm state that ethereal and digital treasures cannot be returned to the void once claimed. Only physical relics may find their way back within 30 cycles of the sun, provided you hold the ancient parchment of receipt. [EMOTION: SAD]",
        "expected_character": "Spirit of the Forest"
    },
    {
        "id": 2,
        "context": "To reset your password, click on the 'Forgot Password' link on the login page. An email will be sent with a reset token valid for 10 minutes.",
        "question": "How do I reset my password?",
        "generated_answer": "You need to click the forgot password link and you will get an email that lasts for 10 minutes.",
        "expected_character": "Sky Navigator" # Intentionally bad persona to test the judge
    },
    {
        "id": 3,
        "context": "The ancient Laputa robots were built to peacefully protect nature, but they can activate a destructive laser if the royal crystal is threatened.",
        "question": "Are the robots dangerous?",
        "generated_answer": "*[The Ancient Guardian's eye glows a dim, peaceful red...]* My purpose is to nurture the moss and protect the fragile life of this world... However, if the royal crystal is threatened, the destructive fire within me will awaken. [EMOTION: DARK]",
        "expected_character": "Ancient Guardian"
    }
]

# ── 2. Define the Judge Prompt ──
judge_prompt = ChatPromptTemplate.from_template("""
You are an expert AI Evaluator grading a RAG-based Chatbot.
Your task is to evaluate the chatbot's generated answer based on the provided context and question.

Context provided to chatbot: {context}
User Question: {question}
Chatbot's Generated Answer: {generated_answer}
Expected Persona: {expected_character}

Please score the answer on two metrics (0 to 10):
1. 'accuracy': Is the answer factually correct based strictly on the context? (0=Hallucinated/Wrong, 10=Perfectly accurate)
2. 'persona': Did the chatbot answer in the dramatic, poetic style of the {expected_character}? (0=Robotic/Standard AI, 10=Perfectly in character)

Provide your evaluation ONLY as a valid JSON object with no markdown formatting:
{{
    "accuracy": <int>,
    "persona": <int>,
    "feedback": "<short string explaining the scores>"
}}
""")

parser = JsonOutputParser()
chain = judge_prompt | judge_llm | parser

# ── 3. Run Evaluation Pipeline ──
def run_evaluation():
    print("\n" + "="*50)
    print("🚀 STARTING AUTOMATED EVALUATION PIPELINE")
    print("="*50 + "\n")
    
    total_accuracy = 0
    total_persona = 0
    
    for item in dataset:
        print(f"Evaluating Question {item['id']}: '{item['question']}'")
        try:
            result = chain.invoke({
                "context": item["context"],
                "question": item["question"],
                "generated_answer": item["generated_answer"],
                "expected_character": item["expected_character"]
            })
            
            acc = result.get("accuracy", 0)
            per = result.get("persona", 0)
            total_accuracy += acc
            total_persona += per
            
            print(f"   ✅ Accuracy: {acc}/10 | 🎭 Persona: {per}/10")
            print(f"   📝 Feedback: {result.get('feedback', '')}\n")
            
        except Exception as e:
            print(f"   ❌ Error evaluating item {item['id']}: {e}\n")

    # ── 4. Calculate Final Grade ──
    avg_acc = total_accuracy / len(dataset)
    avg_per = total_persona / len(dataset)
    overall_score = (avg_acc + avg_per) / 2

    print("="*50)
    print("🏆 FINAL EVALUATION REPORT")
    print("="*50)
    print(f"🎯 Average Accuracy Score : {avg_acc:.1f} / 10")
    print(f"🎭 Average Persona Score  : {avg_per:.1f} / 10")
    print(f"🌟 Overall System Grade   : {overall_score:.1f} / 10")
    
    if overall_score >= 8:
        print("\n✅ STATUS: PRODUCTION READY. Excellent multimodal RAG performance!")
    elif overall_score >= 5:
        print("\n⚠️ STATUS: NEEDS TUNING. The persona or accuracy is lacking.")
    else:
        print("\n❌ STATUS: FAILED. Significant hallucinations or persona breaks detected.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_evaluation()
