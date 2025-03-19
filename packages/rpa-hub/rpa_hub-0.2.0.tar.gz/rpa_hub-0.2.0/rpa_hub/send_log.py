import requests

def send_log_row(token, url, id_rpa, log_data):
    url = f"{url}/rpa/log-row/{id_rpa}"
    if "data" not in log_data or "status" not in log_data or "message" not in log_data:
        return {"error": "Falta a informação de status ou de data ou de message no log_data"}, {"created": False}
    payload = {
        "Id": id_rpa,
        "LogData": log_data
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception as e:
        return {"error": e}, {"created": False}
    if not response.ok:
        return response.json(), {"created":False}
    
    return {"error": ""}, {"created": True}

def send_log_ins(token:str, url:str, id_rpa:int, status:bool, message:str, traceback:str):
    if status:
        status_text = "SUCESSO"
    else:
        if traceback == "":
            return {"error": "Falta a informação do traceback"}, {"created": False}
        status_text = "ERRO"
     
    if message == "":
        return {"error": "Falta a informação da mensagem"}, {"created": False}
    url = f"{url}/rpa/log-row/{id_rpa}"
    payload = {
        "Id": id_rpa,
        "Status": status_text,
        "Message": message,
        "Traceback": traceback
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception as e:
        return {"error": e}, {"created": False}
    if not response.ok:
        return response.json(), {"created":False}
    
    return {"error": ""}, {"created": True}