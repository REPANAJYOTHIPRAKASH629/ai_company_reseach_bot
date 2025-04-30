import streamlit as st
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
	st.error("GOOGLE_API_KEY not found. Please create a .env file with it.")
	st.stop()


# configure the gemini client
genai.configure(api_key=GOOGLE_API_KEY)


# Load Gemini 1.5 pro latest model
model = genai.GenerativeModel("gemini-1.5-pro-latest")


# set up Streamlit page
st.set_page_config(page_title="Gemini Market Research Bot")
st.title("Gemini Market Research Bot")


# input field for company name
company = st.text_input("Enter the company name : ", value="Alphabet")


if st.button("Generate Report"):
	with st.spinner("Generating company research report..."):
		try:
			# prompt for the model
			prompt = f'''
				you are an expert market analyst. Write a short research report on the company : {company}. Include current performance, recent news, and relevant financials. Start your report after a line with '---' and include no extra text after the report. '''
			# generate content from gemini
			response = model.generate_content(prompt)
			full_text = response.text

			# Extract report after '---'
			match = re.search(r"(?<=---\n)(.*)", full_text, re.DOTALL)
			if match:
				report = match.group(1).strip()
				st.markdown("### Company report")
				st.markdown(report)
		
				# save report locally
				with open("company_report.txt", "w", encoding="utf-8") as f:
					f.write(report)
				st.success("Report saved to 'company_report.txt'")
			else:
				st.markdown(full_text)
		except Exception as e:
			st.error(f"X Error: {e}")