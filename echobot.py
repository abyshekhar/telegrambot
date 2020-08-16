import json
import requests
import time
import urllib
from datetime import datetime
import pytz


def greetMsg():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_object = datetime.now(IST)
    hour = datetime_object.hour
    if(hour > 0 and hour < 12):
        return 'Good Morning'
    elif(hour >= 12 and hour < 18):
        return 'Good Afternoon'
    elif hour >= 18 and hour < 22:
        return 'Good Evening'
    else:
        return 'I am sleepy, Good Night!!!'


with open('secrets.json') as f:
    data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
# print(data)

TOKEN = data["key"]
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

greetings = ["Hi", "Hello", "Hey"]


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            msgR = update["message"]["text"]
            value = [1 for item in greetings if(item in msgR)]
            if(1 in value):
                firstname = update["message"]["from"]["first_name"]
                message = "Hi {0},\n{1}".format(firstname, greetMsg())
                text = message
            else:
                text = update["message"]["text"]

            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
