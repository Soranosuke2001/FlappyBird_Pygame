from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

@app.route('/')
def home():
    # saving the json contents to a variable
    with open('./database/scores.json', 'r') as readFile:
        score_List = json.load(readFile)
        sorted_Score_List = sorted(score_List, reverse=True, key=lambda x: x["score"])
        
    return render_template('home.html', sorted_Score_List=sorted_Score_List)

@app.route('/submitscore', methods=['POST'])
def submit():
    data = request.json

    # read the contents of the scores.json file
    with open('./database/scores.json', 'r') as readFile:
        score_List = json.load(readFile)

    # creating the instance of the user score
    user_Score = {
        "username": data["username"],
        "score": data["score"]
    }
    
    # adds the score to the score list
    score_List.append(user_Score)
    
    # writes the new score that was added to the database
    with open('./database/scores.json', 'w') as writeFile:
        json.dump(score_List, writeFile)        

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)