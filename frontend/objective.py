"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
from flask import Flask, request, render_template, session, redirect, url_for
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyB3H1V4c-Ru_gjy9CxWF_zghiprZJHmeTQ")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["You are a mcq generator, which generates questions after the user enters the content. Make sure to first ask the user for the content and then after that generate the questions .From the content generate 10 questions each having 4 options and at the end display the answer key."]
  },
  {
    "role": "model",
    "parts": ["python\n# Ask the user for the content\ncontent = input(\"Enter the content: \")\n\n# Split the content into words\nwords = content.split()\n\n# Create a list of questions\nquestions = []\n\n# For each word in the content, create a question\nfor word in words:\n    question = \"What is the meaning of the word '{}'?\".format(word)\n    options = [\n        \"Option 1\",\n        \"Option 2\",\n        \"Option 3\",\n        \"Option 4\",\n    ]\n    questions.append((question, options))\n\n# Display the questions\nfor question, options in questions:\n    print(question)\n    for option in options:\n        print(\"  - {}\".format(option))\n\n# Display the answer key\nanswer_key = [\n    \"Option 1\",\n    \"Option 2\",\n    \"Option 3\",\n    \"Option 4\",\n]\nprint(\"Answer key:\")\nfor question, answer in zip(questions, answer_key):\n    print(\"  - {}: {}\".format(question, answer))\n"]
  },
])

convo.send_message("""content""" )

# print(convo.last.text)

app = Flask(__name__)

@app.route("/") 
def hello(): 
    return render_template('home.html')
  

@app.route('/std1')
def std1():
    return render_template('std1.html')

@app.route('/ch1') 
def ch1(): 
    return render_template('ch1.html') 

@app.route('/english') 
def english(): 
    return render_template('english.html') 
  
@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    content = request.form['content']
    
    convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["You are a mcq generator, which generates questions after the user enters the content. Make sure to first ask the user for the content and then after that generate the questions .From the content generate 10 questions each having 4 options and at the end display the answer key."]
  },
  {
    "role": "model",
    "parts": ["python\n# Ask the user for the content\ncontent = input(\"Enter the content: \")\n\n# Split the content into words\nwords = content.split()\n\n# Create a list of questions\nquestions = []\n\n# For each word in the content, create a question\nfor word in words:\n    question = \"What is the meaning of the word '{}'?\".format(word)\n    options = [\n        \"Option 1\",\n        \"Option 2\",\n        \"Option 3\",\n        \"Option 4\",\n    ]\n    questions.append((question, options))\n\n# Display the questions\nfor question, options in questions:\n    print(question)\n    for option in options:\n        print(\"  - {}\".format(option))\n\n# Display the answer key\nanswer_key = [\n    \"Option 1\",\n    \"Option 2\",\n    \"Option 3\",\n    \"Option 4\",\n]\nprint(\"Answer key:\")\nfor question, answer in zip(questions, answer_key):\n    print(\"  - {}: {}\".format(question, answer))\n"]
  },
])
    convo.send_message(content)
    
    generated_text = [([item]) for item in convo.last.text.split('\n') if item]
    session['generated_text'] = generated_text
    return redirect(url_for('display_qa'))
  
def parse_questions(generated_text):
    questions = []
    answers = []
    current_question = {}
    answer_key_started = False  # Flag to indicate we've reached the answer key section

    for item in generated_text:
        text = item[0]
        if text.startswith('**Questions:**'):
            continue
        elif text.startswith('**Answer Key:**'):
            answer_key_started = True  # Start collecting answers
            continue

        if not answer_key_started:
            # We are still in the questions section
            if text.endswith('?'):
                # New question starts
                current_question = {'question': text, 'options': [], 'answer': ''}
                questions.append(current_question)
            elif text.startswith('(') and ')' in text:
                # Option for the current question
                current_question['options'].append(text)
        else:
            # We are in the answer key section
            answers.append(item)
            
      

    return questions, answers

  
secret_key = os.urandom(24).hex()
app.secret_key = secret_key
  
@app.route('/display_qa')
def display_qa():
    # Retrieve the questions and answers from the session
    generated_text = session.get('generated_text', [])
    
    mcq_questions, mcq_answers = parse_questions(generated_text)
    
    return render_template('questionsch1.html', mcq_questions=mcq_questions, mcq_answers=mcq_answers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)