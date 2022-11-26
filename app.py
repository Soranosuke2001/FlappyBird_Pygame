from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    # saving the json contents to a variable
    with open('./database/scores.json', 'r') as readFile:
        score_List = json.load(readFile)
        sorted_Score_List = sorted(score_List, reverse=True, key=lambda x: x["score"])
    return render_template('home.html', sorted_Score_List=sorted_Score_List)

if __name__ == '__main__':
    app.run(debug=True)