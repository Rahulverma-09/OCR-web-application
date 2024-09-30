# Importing Essential Libraries
import streamlit as st
import pytesseract
from PIL import Image
from googletrans import Translator

# Configuration of Pytesseract
tessdata_directory = r'C:\\Program Files\\Tesseract OCR\\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract OCR\\tesseract.exe'


# Define function to display response and keyword searching
def display_text(extracted_text, translated_text):
    st.subheader('The Extracted Text : ')
    st.write(extracted_text)

    st.subheader('The Translated Text : ')
    st.write(translated_text)

    # Keyword Searching
    keywords = st.text_input("Enter keyword : ")
    if keywords:
        if keywords in extracted_text or keywords in translated_text:
            st.success("Keywords found")
            st.write(f"Keywords :- ",keywords)
        else:
            st.error("Keywords not found") 

    return extracted_text 


# Define function to detect and translate language
def languag_detection(extracted_text):
    trans=Translator()
    detected_language = trans.detect(extracted_text)
    detected_language = detected_language.lang

    if detected_language == 'en':
        translated_text = trans.translate(extracted_text,dest='hi')
        translated_text = translated_text.text 
        
        # Function calling to display response
        display_text(extracted_text,translated_text)

    elif detected_language == 'hi':
        translated_text = trans.translate(extracted_text,dest='en')
        translated_text = translated_text.text

        # Function calling to display response
        display_text(extracted_text,translated_text)

    else:
        st.error('Oops! something else :(')


# Define function to perform OCR 
def optical_char_recognition(image_path):
    extracted_text = pytesseract.image_to_string(image_path,lang='eng+hin')

    if extracted_text:
        # Function calling to detect language
        languag_detection(extracted_text)
    else:
        st.error("Sorry, didn't get text :(")


# Initialize Streamlit Application---

st.set_page_config(page_title="www.optical-character-recognition.page")
st.header("OCR & KEYWORD SEARCH")
uploaded_file = st.file_uploader("Upload Image",type=['jpg','jpeg','png'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img,caption="uploaded image",use_column_width=True)

    # Function calling to perform OCR
    optical_char_recognition(img)