import streamlit as st
import PyPDF2
import  os
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Critiquer", page_icon="📜", layout="wide")

st.title("Resume Critiquer 📜")
st.markdown("Upload your resume in PDF or TXT format and get feedback on how to improve it.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf","txt"])
job_role = st.text_input("Enter the job role you are applying for (optional)", placeholder="e.g., Software Engineer")

analyze= st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text=""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read. Please upload a valid PDF or TXT file.")
            st.stop()
        
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations."""
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant that provides feedback on resumes."}
                ,{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        st.markdown("### Analysis Result")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An error occurred while processing your resume: {str(e)}")
