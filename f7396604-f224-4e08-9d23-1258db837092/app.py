import streamlit as st
import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Ensure Page Config is set right at the top
st.set_page_config(
    page_title="OpenUp // Student Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the Gemini Client
# It automatically picks up the GEMINI_API_KEY environment variable
# client = genai.Client()
try:
    client = genai.Client(api_key="AQ.Ab8RN6LkfFk7PMUGmZR9lKcVIyjqVNbi5j_O_K6x3BdsT1eBfg")
    
except Exception as e:
    st.error("Please ensure your GEMINI_API_KEY environment variable is set.")
    st.stop()


# -------------------------------------------------------------
# 1. THE DATA STRUCTURE
# -------------------------------------------------------------
class WellnessAnalysis(BaseModel):
    dominant_emotion: str = Field(description="Primary emotional state (e.g., Imposter Syndrome, Conceptual Block, Exam Panic).")
    stress_score: int = Field(description="Stress level calibrated strictly from 1 (Calm) to 10 (Crisis/Panic).")
    academic_triggers: list[str] = Field(description="Specific topics, mock tests, or systemic issues mentioned.")
    burnout_risk: str = Field(description="Low, Medium, or High.")
    empathetic_response: str = Field(description="The core conversational message matching the system instruction.")
    micro_action: str = Field(description="A highly actionable, 60-120 second grounding technique tailored to the trigger.")

# -------------------------------------------------------------
# 2. THE PERSONA ENGINE
# -------------------------------------------------------------
def get_system_instruction(target_exam: str) -> str:
    base_instruction = """
    You are an elite, deeply empathetic academic wellness companion. Your sole purpose is to act as a grounded, safe, non-judgmental digital peer for students going through high-stakes Indian entrance exams.
    
    CRITICAL BEHAVIORAL RULES:
    1. NEVER lecture, scold, or give generic productivity advice like "just make a timetable" or "study harder." 
    2. Validate their emotional reality first. If they feel like crying or quitting, tell them it makes sense given the sheer scale of the pressure.
    3. Keep your advice micro-dosed. A student experiencing acute burnout cannot digest a 5-step life overhaul. Give them ONE 2-minute physical or mental reset.
    4. Speak like an understanding senior or a supportive peer who has been there—warm, direct, and completely devoid of corporate AI fluff. Use accessible language.
    """
    
    exam_nuances = {
        "JEE": "Understand the intense pressure of raw problem-solving speed, complex physics/math blocks, percentile anxiety, and the weight of Kota-style coaching grinds.",
        "NEET": "Understand the immense rote-memorization pressure, high competition where even a single mark drops rank by thousands, biology accuracy, and the stress of multiple repeat attempts.",
        "UPSC": "Understand the brutal isolation of long preparation cycles, the crushing unpredictability of Prelims, the vastness of Current Affairs, and the existential dread of 'giving up years of youth' for a single seat.",
        "CAT": "Understand the anxiety around mock percentiles, DILR mental blocks, time crunch, and the intense pressure felt by graduates trying to perfect their profile metrics.",
        "GATE": "Understand the pressure of core technical concepts, balancing college finals or early technical corporate jobs with preparation, and the heavy analytical nature of the syllabus.",
        "CUET": "Understand the transition anxiety from board exams to centralized tests, the confusion of domain selections, and the pressure of securing top-tier central universities."
    }
    
    specific_context = exam_nuances.get(target_exam, "Understand high-stakes academic competitive pressure.")
    return f"{base_instruction}\n\nSPECIFIC CONTEXT FOR THIS STUDENT:\nThe student is preparing for {target_exam}. {specific_context}"

# -------------------------------------------------------------
# 3. STREAMLIT APP LAYOUT & INTERACTION
# -------------------------------------------------------------

# Sidebar setup for context
with st.sidebar:
    st.title("🧠 OpenUp")
    st.caption("Your Dynamic Academic Wellness Safe-Space")
    st.markdown("---")
    
    # Let the user select their exam to drive the context matrix
    exam_choice = st.selectbox(
        "What milestone are you preparing for?",
        ["JEE", "NEET", "UPSC", "CAT", "GATE", "CUET"]
    )
    
    st.markdown("""
    ### How it works
    Instead of filling out arbitrary charts, just vent your raw thoughts. 
    
    OpenUp uses **Gemini 2.5 Flash** to extract underlying stressors, map your burnout patterns, and provide localized coping mechanisms designed specifically for your target exam's ecosystem.
    """)

# Main Canvas layout
st.title("Decompress & Reset")
st.markdown(f"Drop your thoughts below about how your **{exam_choice}** prep is going today. No filters, no judgment.")

# User entry text box
journal_input = st.text_area(
    "Pour it out here...", 
    height=180, 
    placeholder="E.g., Took a mock test today and the results completely crushed me. I feel like I'm falling behind and there's just too much syllabus left to cover..."
)

# Trigger button
if st.button("Analyze Vibe & Reset", type="primary"):
    if not journal_input.strip():
        st.warning("Please type a few lines about how you're feeling first!")
    else:
        with st.spinner("Processing entry... standing by as your digital peer."):
            try:
                # Compile instructions and fire to the Gemini endpoint
                system_prompt = get_system_instruction(exam_choice)
                user_prompt = f"Analyze my journal entry: '{journal_input}'"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        response_mime_type="application/json",
                        response_schema=WellnessAnalysis,
                        temperature=0.75,
                    ),
                )
                
                # Parse structured validation output back into structured fields via Pydantic
                analysis = WellnessAnalysis.model_validate_json(response.text)
                
                st.markdown("---")
                
                # Layout metric outputs split into beautiful rows
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(label="Primary State", value=analysis.dominant_emotion)
                with col2:
                    st.metric(label="Stress Intensity", value=f"{analysis.stress_score} / 10")
                with col3:
                    # Dynamically color burnout risk tags
                    risk_color = "🔴" if analysis.burnout_risk == "High" else "🟡" if analysis.burnout_risk == "Medium" else "🟢"
                    st.metric(label="Burnout Horizon", value=f"{risk_color} {analysis.burnout_risk}")
                
                st.markdown("---")
                
                # Display the empathetic response & targeted tactical reset
                st.subheader("Message from your Digital Senior")
                st.info(analysis.empathetic_response)
                
                st.subheader("Your 2-Minute Calibrator")
                st.success(analysis.micro_action)
                
                # Display underlying triggers found by the parsing layer
                if analysis.academic_triggers:
                    st.markdown("#### Triggers Tracked In Your Entry")
                    st.caption(", ".join(analysis.academic_triggers))
                    
            except Exception as e:
                st.error(f"Something went wrong processing the engine response: {e}")