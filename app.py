from flask import Flask, render_template, request, redirect, session, url_for
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
def submitscore():
    data = request.json
    print(data)

    # read the contents of the scores.json file
    score_List = updateDB('./database/scores.json', 'r')

    # gets the list of users in the scores.json file
    user_List = score_List.keys()

    # if the username already exists, add the score to the list of scores in the database
    if len(score_List[data['username']]) > 0:

        print(score_List[data["username"]][-1])

        id = score_List[data["username"]][-1]["id"] + 1

        score_Info = {
            "id": id,
            "score": data["score"],
            "date": data["date"]
        }

        score_List[data["username"]].append(score_Info)
    
    else:
        # creating the instance of the user score
        user_Score = {
            "id": 1,
            "score": data["score"],
            "date": data["date"]
        }

        score_List[data["username"]].append(user_Score)

    # writes the new score that was added to the database
    updateDB('./database/scores.json', 'w', score_List)

    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users_List = updateDB('./database/users.json', 'r')

        for user in users_List:

            # directs the user to the personal page to view the scores or delete them
            if user["username"] == username and user["password"] == password:
                session['username'] = username
                return redirect(url_for('profile'))
    
        # redirects the user back to the login page if the username or password is invalid
        error = 'Invalid Username or Password'
        return render_template('login.html', error=error)

    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('profile'))
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        # reads the list of users in the database
        users_List = updateDB('./database/users.json', 'r')

        # checks if the username already exists
        for user in users_List:

            # returns an error message to the user if the username already exists
            if user['username'] == request.form['username']:
                error = "Username already exists"
                return render_template('register.html', error=error)

        # creating the dictionary for the new user
        new_User = {
            "username": request.form['username'],
            "password": request.form['password']
        }

        # adding the new user to the list of users and updating the database
        users_List.append(new_User)
        updateDB('./database/users.json', 'w', users_List)

        # updating the score database to add the new user
        score_List = updateDB('./database/scores.json', 'r')

        # creating a new list of scores for the new user and updating the database
        new_Score = {
            f'{request.form["username"]}': []
        }

        score_List.update(new_Score)
        updateDB('./database/scores.json', 'w', score_List)
        return render_template('login.html')

@app.route('/profile')
def profile():
    username = session.get('username', None)
    score_List = updateDB('./database/scores.json', 'r')
    user_Scores = score_List[username]
    return render_template('profile.html', user_Scores=user_Scores, username=username)

@app.route('/delete/score', methods=['POST'])
def deleteScore():
    # print(request.form)
    id = int(request.form.to_dict()["delete"])
    username = request.form["username"]

    score_List = updateDB('./database/scores.json', 'r')

    for score in score_List[username]:
        print(score)
        if score["id"] == id:
            score_List[username].remove(score)

    updateDB('./database/scores.json', 'w', score_List)
    return redirect(url_for('profile'))

# method to read or write the json file from the database
def updateDB(database, method, updateJSON=None):

    # reads the database if the method is read
    if method == 'r':
        with open(database, 'r') as readFile:
            score_List = json.load(readFile)
            return score_List

    # writes to the database if the method is write
    elif method == 'w':
        with open(database, 'w') as writeFile:
            json.dump(updateJSON, writeFile)

    else:
        print('There was an error')
        return None

if __name__ == '__main__':
    app.run(debug=True)