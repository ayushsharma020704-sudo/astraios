import requests
import json

def test_api():
    print("Testing POST /mission/plan...")
    try:
        response = requests.post(
            "http://localhost:8000/mission/plan",
            json={"goal": "Design a mission to Kepler-452b"},
            timeout=180
        )
        print(f"Status Code: {response.status_code}")
        print("Raw Response Output:")
        print(response.text)
    except Exception as e:
        print(f"Connection/Exception Error: {e}")

if __name__ == "__main__":
    test_api()
