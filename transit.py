import requests
import os

# Get API key from environment variable API_KEY, requires a .env file in the same directory
API_KEY = os.getenv("API_KEY")

# Given a station ID (id), return a list of times, in minutes, for the next trains arriving at that station
# if the time is -1, there are no trains arriving at that station
def get_train(id):
    next_train = requests.get(f"https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{id}", headers={"api_key" : API_KEY})

    if next_train.status_code == 200:
        pass
    else:
        raise ValueError("The URL is invalid")

    next_train = next_train.json()
    train_times = []

    for train in next_train["Trains"]:
        time = train["Min"]
        # if data is passed as '', interpret as no data and skip
        if time == '':
            continue
        else:
            pass
        train_times.append(int(time))

    return train_times

print(get_train("A01"))
