import requests

# Example: fetch data from GitHub API and print the response status and JSON keys
url = "https://api.github.com"
try:
    response = requests.get(url, timeout=10)
    print(f"Status code: {response.status_code}")
    # Print top-level keys of JSON response if available
    try:
        data = response.json()
        print("Top-level JSON keys:", list(data.keys()))
    except ValueError:
        print("Response is not JSON.")
except requests.RequestException as e:
    print("An error occurred:", e)
