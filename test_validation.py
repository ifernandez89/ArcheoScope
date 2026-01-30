
import requests
import json

BASE_URL = "http://localhost:8003"

def test_coordinate_validation():
    print("Testing coordinate validation (invalid latitude)...")
    payload = {
        "lat_min": 99.0,
        "lat_max": 100.0,
        "lon_min": -50.0,
        "lon_max": -49.0,
        "region_name": "Invalid Lat Test"
    }
    response = requests.post(f"{BASE_URL}/api/scientific/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_area_validation():
    print("\nTesting area validation (excessive area)...")
    payload = {
        "lat_min": -10.0,
        "lat_max": 10.0, # 20 degrees difference
        "lon_min": -10.0,
        "lon_max": 10.0, # 20 degrees difference
        "region_name": "Large Area Test"
    }
    response = requests.post(f"{BASE_URL}/api/scientific/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    try:
        test_coordinate_validation()
        test_area_validation()
    except Exception as e:
        print(f"Error connecting to server: {e}")
