from datetime import datetime

today = datetime.now()
x = today.strftime("%m-%d-%Y %H:%M")

print(today)
print(x)