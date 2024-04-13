"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
from flask import Flask, request, jsonify
import google.generativeai as genai

genai.configure(api_key="AIzaSyDpNYPoa5g5Fd3h642J31kZdXiKUQ2BIj0")

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

print(convo.last.text)

app = Flask(__name__)

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    content = request.json['content']
    convo = model.start_chat(history=[
        # Your existing conversation history setup
    ])
    convo.send_message(content)
    questions = convo.last.text  # This will contain the generated questions
    return jsonify(questions)

if __name__ == '__main__':
    app.run()