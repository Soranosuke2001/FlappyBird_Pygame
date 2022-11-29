from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

@app.route('/')
def home():
    # saving the json contents to a variable
    with open('./database/scores.json', 'r') as readFile:
        score_List = json.load(readFile)
        users = score_List.keys()

        sorted_List = []

        # sorting functionalty to sort from greatest to least in score
        for user in users:
            for score in score_List[user]:
                user_Score = {
                    "username": user,
                    "score": score["score"],
                    "date": score["date"]
                }
                sorted_List.append(user_Score)

        sorted_List = sorted(sorted_List, key=lambda x: x["score"], reverse=True)

    return render_template('home.html', sorted_List=sorted_List)

@app.route('/submitscore', methods=['POST'])
def submit():
    data = request.json

    # read the contents of the scores.json file
    with open('./database/scores.json', 'r') as readFile:
        score_List = json.load(readFile)

    # gets the list of users in the scores.json file
    user_List = score_List.keys()

    # if the username already exists, add the score to the list of scores in the database
    if data["username"] in user_List:

        score_Info = {
            "score": data["score"],
            "date": data["date"]
        }

        score_List[data["username"]].append(score_Info)
    
    else:
        # creating the instance of the user score
        user_Score = [{
                "score": data["score"],
                "date": data["date"]
        }]

        score_List[data["username"]] = user_Score

    # writes the new score that was added to the database
    with open('./database/scores.json', 'w') as writeFile:
        json.dump(score_List, writeFile)        

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)