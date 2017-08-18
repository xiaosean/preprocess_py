import os
import time
import requests

while not "xgboost_without_infre_all_0_0805.model" in os.listdir("."):
	print("not found")
	time.sleep(60)

print("file found")

requests.post(
    "https://api.mailgun.net/v3/sandboxe9bb891a60414f4bae93f2cc55daa963.mailgun.org/messages",
    auth=("api", "key-a007a22faf334a3510137b6cc03c21a6"),
    data={"from": "Mailgun Sandbox <postmaster@sandboxe9bb891a60414f4bae93f2cc55daa963.mailgun.org>",
          "to": "Toby <atch84@gmail.com>",
          "subject": "XGBoost Result",
          "text": "FINININININISH"})