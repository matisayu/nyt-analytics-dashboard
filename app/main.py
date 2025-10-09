import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NYT_API_KEY")
period = 1
url = f"https://api.nytimes.com/svc/mostpopular/v2/viewed/{period}.json"

res = requests.get(url, params={"api-key": API_KEY})
data = res.json()

print(len(data["results"]), "articles fetched")
