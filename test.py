def alphaSort(score_List, method):
    if method == 'a-z':
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

        user_List = []
        for user in sorted_List:
            user_List.append(user['username'])

        name_Sorted = sorted(user_List, reverse=False)

        sorted_Dict = []
        for user in name_Sorted:
            for og_User in sorted_List:
                if user == og_User['username']:
                    sorted_Dict.append(og_User)
        print(sorted_Dict)


dict = {
    "sora": [],
    "tom": [
        {
            "id": 1,
            "score": 20,
            "date": "12-01-2022 12:00"
        }
    ],
    "hello": [
        {
            "id": 1,
            "score": 0,
            "date": "11-29-2022 1:22"
        }
    ]
}

alphaSort(dict, 'a-z')
