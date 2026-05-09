import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from services.llm_service import extract_claims, verify_claim
from services.search_service import perform_web_search

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Fact-Check Agent", page_icon="🔍", layout="wide")

st.title("🔍 Fact-Check Agent")
st.markdown("Upload a PDF to verify its factual claims against the live web.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    st.info("This agent uses OpenRouter and Tavily Search to verify facts.")
    st.divider()
    

# --- MAIN INTERFACE ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # 1. Process PDF
    with st.status("Reading PDF content...", expanded=True) as status:
        text = extract_text_from_pdf(uploaded_file)
        st.write("Extracting claims...")
        
        # 2. Extract Claims
        claims = extract_claims(text)
        status.update(label="Claims extracted! Starting verification...", state="running")
        
        # 3. Verification Loop
        results = []
        for i, item in enumerate(claims):
            claim_text = item['claim']
            st.write(f"Verifying Claim {i+1}: {claim_text[:60]}...")
            
            # Search web
            evidence, sources = perform_web_search(claim_text)
            
            # Verify via LLM
            verdict_data = verify_claim(claim_text, evidence)
            verdict_data['sources'] = sources
            verdict_data['original_claim'] = claim_text
            results.append(verdict_data)
            
        status.update(label="Verification Complete!", state="complete", expanded=False)

    # --- DISPLAY RESULTS ---
    st.divider()
    st.subheader("Verification Report")

    for res in results:
        # Determine color based on verdict
        color = "green" if res['verdict'] == "VERIFIED" else "orange" if res['verdict'] == "INACCURATE" else "red"
        
        with st.expander(f"[{res['verdict']}] - {res['original_claim'][:100]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Verdict:** :{color}[{res['verdict']}]")
                st.markdown(f"**Corrected Fact:** {res['corrected_fact']}")
                st.markdown(f"**Explanation:** {res['explanation']}")
            
            with col2:
                st.metric("Confidence Score", res['confidence'])
                st.write("**Sources:**")
                for link in res['sources']:
                    st.markdown(f"- [Link]({link})")

else:
    st.warning("Please upload a PDF file to begin.")