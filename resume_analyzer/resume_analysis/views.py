from django.shortcuts import render
from django.http import JsonResponse
import joblib
import os
from PyPDF2 import PdfReader
from docx import Document
from .models import Resume, ResumeFeedback
from pdfminer.high_level import extract_text


# Define the path to your model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'nlp_model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

# Load the model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def index(request):
    return render(request, 'resume_analysis/index.html')

def extract_text_from_pdf(file):
    text = ""
    reader = PdfReader(file)
    print(reader)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def predict(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        uploaded_file = request.FILES.get('file')

        # Check if a file is uploaded
        if uploaded_file:
            if uploaded_file.name.endswith('.pdf'):
                text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.name.endswith('.docx'):
                text = extract_text_from_docx(uploaded_file)

        processed_text = vectorizer.transform([text])
        prediction = model.predict(processed_text)

        # Save feedback if provided
        resume = Resume.objects.create(text=text)

        feedback = request.POST.get('feedback')
        if feedback is not None:
            ResumeFeedback.objects.create(resume=resume, prediction=prediction[0], correct=(feedback == 'true'))
        return JsonResponse({'prediction': prediction[0]})
    
