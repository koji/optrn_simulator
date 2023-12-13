import uuid
import requests

def generate_unique_name():
    unique_name = str(uuid.uuid4()) + ".py"
    return unique_name

def send_post_request(payload):
    url = "https://baxin-simulator.hf.space/protocol"
    protocol_name = generate_unique_name()
    data = {"name": protocol_name, "content": payload}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        print("Error: " + response.text)
        return "Error: " + response.text

    response_data = response.json()
    if "error_message" in response_data:
        print("Error in response:", response_data["error_message"])
        return response_data["error_message"]
    elif "protocol_name" in response_data:
        return response_data["run_status"]
    else:
        print("Unexpected response:", response_data)
        return "Unexpected response"

def send_code(text):
   response = send_post_request(text)
   return response
