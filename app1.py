import streamlit as st
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY not found. Please create a .env file with it.")
    st.stop()

# Configure the Gemini client
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Set up Streamlit page
st.set_page_config(page_title="📊 Gemini Market Research Bot", layout="centered")
st.title("📈 Gemini Market Research Bot")

# Input field
company = st.text_input("🔍 Enter the company name:", value="Alphabet")

# Report generation logic
if st.button("🚀 Generate Report"):
    with st.spinner("Generating company research report..."):
        try:
            prompt = f"""
                You are an expert market analyst. Write a short research report on the company: {company}.
                Include current performance, recent news, and relevant financials.
                Start your report after a line with '---' and include no extra text after the report.
            """
            response = model.generate_content(prompt)
            full_text = response.text

            # Extract report after '---'
            match = re.search(r"(?<=---\n)(.*)", full_text, re.DOTALL)
            if match:
                report = match.group(1).strip()

                st.markdown("### 🧾 Company Report")
                st.markdown(f"<div style='background-color:#f0f2f6; padding:15px; border-radius:10px'><pre>{report}</pre></div>", unsafe_allow_html=True)

                # Save to file and provide download link
                report_filename = f"{company.lower().replace(' ', '_')}_report.txt"
                with open(report_filename, "w", encoding="utf-8") as f:
                    f.write(report)

                with open(report_filename, "rb") as file:
                    st.download_button(
                        label="📥 Download Report",
                        data=file,
                        file_name=report_filename,
                        mime="text/plain"
                    )
                st.success("✅ Report generated successfully!")
            else:
                st.warning("⚠️ Report format not as expected. Full output shown below:")
                st.markdown(full_text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
