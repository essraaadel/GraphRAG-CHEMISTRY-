import streamlit as st
import time
from database import db
from chain import generate_cypher
from answer_chain import generate_final_answer

# --- Page Config & Styling ---
st.set_page_config(
    page_title="GraphRAG | Scientific Chatbot",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for Premium Design & Compatibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2f, #121212);
        color: #ffffff;
    }
    
    .chat-bubble {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        padding: 15px;
        margin: 10px 0;
    }
    
    .user-bubble {
        border-left: 5px solid #6366f1;
    }
    
    .assistant-bubble {
        border-left: 5px solid #a855f7;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    h1 {
        background: linear-gradient(90deg, #fff, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    .cypher-box {
        background: #1a1a1a;
        padding: 10px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        color: #10b981;
        border-left: 4px solid #6366f1;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("Admin Console")
    st.info("Manage your Neo4j Knowledge Graph here.")
    
    if st.button("Reset & Seed Database"):
        with st.spinner("Seeding database..."):
            db.seed_data()
        st.success("Graph refreshed with user data.")

# --- Header ---
st.title("🧬 GraphRAG Scientific Intelligence")
st.markdown("Interact with your **Neo4j Pharmacology Knowledge Graph** using GPT-4o.")
st.markdown("---") # Replaced st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History (Using custom bubbles for compatibility)
for message in st.session_state.messages:
    role_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
    st.markdown(f"""
    <div class="chat-bubble {role_class}">
        <strong>{'👤 User' if message['role'] == 'user' else '🤖 Assistant'}</strong><br>
        {message['content']}
    </div>
    """, unsafe_allow_html=True)
    
    if "cypher" in message and message["role"] == "assistant":
        st.markdown(f"<div class='cypher-box'><b>Query:</b> {message['cypher']}</div>", unsafe_allow_html=True)

# --- Input Section ---
# Using a form for input compatibility with older Streamlit versions
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask a question:", placeholder="e.g., How does Fever affect Humans?")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process
    with st.spinner("Analyzing graph..."):
        try:
            # 1. Generate Cypher
            cypher_query = generate_cypher(user_input)
            
            # 2. Execute
            results = db.run_query(cypher_query)
            
            # 3. Final Answer
            final_answer = generate_final_answer(user_input, results)
        except Exception as e:
            final_answer = f"Error: {e}"
            cypher_query = "N/A"

    # Add Assistant Message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": final_answer,
        "cypher": cypher_query
    })
    st.experimental_rerun()

# --- Footer ---
st.markdown("---") # Replaced st.divider()
st.caption("Powered by Azure OpenAI GPT-4o & Neo4j.")
