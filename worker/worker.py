import requests
import schedule
import time

URL = "https://crm-udrl.onrender.com/woker_greeting/"


def send_request():
    try:
        response = requests.post(URL, json={"greet": "hello"})
        print(f"Response ({response.status_code}): {response.text}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        print(time.now())


# Schedule the request every 10 minutes
schedule.every(11).minutes.do(send_request)

while True:
    print("worker initialized")
    schedule.run_pending()
    time.sleep(60*11)
