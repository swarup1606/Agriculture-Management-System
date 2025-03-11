import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini Pro Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(image, prompt):
    response = model.generate_content([prompt, image])
    return response.text

def analyze_plant_disease(image):
    prompt = """
    Analyze this plant image and provide the following information:
    1. Disease Name (if any disease is present)
    2. Factors Causing the Disease
    3. Treatment or Cure
    4. Preventive Measures
    
    Format the response in a clear, structured way with appropriate headings.
    If no disease is detected, please mention that the plant appears healthy.
    """
    return get_gemini_response(image, prompt)

# Set page configuration
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    .upload-box:hover {
        border-color: #45a049;
        background-color: #f0f2f0;
    }
    .title {
        color: #2E7D32;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .subtitle {
        color: #555;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='title'>Plant Disease Detection</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload a plant image to detect diseases and get treatment recommendations</p>", unsafe_allow_html=True)

# File uploader
with st.container():
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Uploaded Plant Image", use_column_width=True)
    
    with col2:
        st.info("Analyzing image... Please wait.")
        try:
            # Get analysis from Gemini
            analysis = analyze_plant_disease(image)
            st.success("Analysis Complete!")
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.stop()
    
    # Display analysis results
    st.markdown("### Analysis Results")
    st.write(analysis)

# Add instructions at the bottom
with st.expander("How to use"):
    st.write("""
    1. Click on 'Browse files' or drag and drop a plant image in the upload box
    2. Wait for the analysis to complete
    3. Review the results, which include:
        - Disease identification
        - Causes of the disease
        - Treatment recommendations
        - Preventive measures
    """)

# Add footer
st.markdown("""
---
<p style='text-align: center; color: #666;'>
    Powered by Google Gemini Pro Vision | Created with Streamlit
</p>
""", unsafe_allow_html=True) 