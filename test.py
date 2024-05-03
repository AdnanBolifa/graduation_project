import requests

url = 'http://127.0.0.1:8000/api/predict/'
data = {
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
}

response = requests.post(url, json=data)
try:
    print(response.json())
except Exception as e:
    print("Error:", e)
    print("Response text:", response.text)
