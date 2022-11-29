from flask import Flask, render_template, request, redirect, flash
import json

app = Flask(__name__)
app.secret_key = '123'

@app.route('/')
def home():
    # saving the json contents to a variable
    score_List = updateDB('./database/scores.json', 'r')
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
    score_List = updateDB('./database/scores.json', 'r')

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
    updateDB('./database/scores.json', 'w', score_List)

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users_List = updateDB('./database/users.json', 'r')

        for user in users_List:
            if user["username"] == username and user["password"] == password:
                score_List = updateDB('./database/scores.json', 'r')
                return render_template('login.html')

            else:
                error = 'Invalid Username or Password'
                return render_template('login.html', error=error)
    
        return render_template('login.html')

    if request.method == 'GET':
        return render_template('login.html')


# method to read or write the json file from the database
def updateDB(database, method, updateJSON=None):
    if method == 'r':
        with open(database, 'r') as readFile:
            score_List = json.load(readFile)
            return score_List

    elif method == 'w':
        with open(database, 'w') as writeFile:
            json.dump(updateJSON, writeFile)

    else:
        print('There was an error')
        return None

if __name__ == '__main__':
    app.run(debug=True)