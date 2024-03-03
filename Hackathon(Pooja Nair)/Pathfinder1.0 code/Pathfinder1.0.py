from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import openai
import json

app = Flask(__name__, template_folder='C:/Users/sally/hackathon')

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hobbies = request.form['hobbies'].split(',')
        interests = request.form['interests'].split(',')
        skills = request.form['skills'].split(',')
        major = request.form['major'].strip()

        user_input = {
            "hobbies": hobbies,
            "interests": interests,
            "skills": skills,
            "major": major
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career counselor providing recommendations based on user's hobbies, interests, skills, and education major."},
                {"role": "user", "content": json.dumps({"input": user_input})},
            ]
        )

        recommendations = completion.choices[0].message.content.strip().split('\n')
        return render_template('index.html', recommendations=recommendations[:5])
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)