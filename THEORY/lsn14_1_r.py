import requests

url = "http://127.0.0.1:8000/ex1/"
res = requests.get(url, headers={"Authorization": "test"})
print(res.status_code)
print(res.json())
