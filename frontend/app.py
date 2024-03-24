from flask import Flask, request, render_template
from transformers import pipeline
import torch
import fitz  # PyMuPDF
import csv
from PIL import Image
import pytesseract

app = Flask(__name__)

# Define the route for the index page
@app.route('/')
def index():
     return render_template('index.html', home_template='home.html')

# Define the route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Initialize the Hugging Face pipeline for summarization
    hf_name = "pszemraj/led-base-book-summary"
    summarizer = pipeline(
        "summarization",
        hf_name,
        device=0 if torch.cuda.is_available() else -1,
    )

    # Get the uploaded file from the request
    uploaded_file = request.files['file']
    
    if uploaded_file.filename != '':
        # Save the uploaded file
        uploaded_file.save(uploaded_file.filename)

        # Process the uploaded file based on its format
        if uploaded_file.filename.endswith(".pdf"):
            text = read_pdf(uploaded_file.filename)
        elif uploaded_file.filename.endswith(".csv"):
            text = read_csv(uploaded_file.filename)
        elif uploaded_file.filename.endswith((".png", ".jpg", ".jpeg")):
            text = read_image(uploaded_file.filename)
        else:
            text = "Unsupported file format."

        # Summarize the text using the Hugging Face pipeline
        summarized_text = summarizer(text)

        # Pass the summarized text to the result page
        return render_template('result.html', summarized_text=summarized_text)
    else:
        return "No file uploaded"

# Function to read PDF
def read_pdf(file_path):
    pdf_text = ""
    pdf_document = fitz.open(file_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pdf_text += page.get_text()

    pdf_document.close()
    return pdf_text

# Function to read CSV
def read_csv(file_path):
    csv_text = ""
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_text += ', '.join(row) + '\n'
    return csv_text

# Function to read image using OCR
def read_image(file_path):
    image_text = pytesseract.image_to_string(Image.open(file_path))
    return image_text

if __name__ == '__main__':
    app.run(debug=True)
