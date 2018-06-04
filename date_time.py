import datetime

yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))
yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")

print(yesterday)
