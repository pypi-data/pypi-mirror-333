import requests


def login(email, password, url):
    url = f"{url}/login"
    body = {
        "Email": email,
        "Password": password
    }
    
    try:
        result = requests.post(url, json=body)
    except Exception as e:
        return {"error": e}, {"authorization":""}
    if not result.ok:
        return result.json(), {"authorization":""}
    result = result.json()
    return {"error": ""}, result
    
