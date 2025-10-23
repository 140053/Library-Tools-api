import requests

url = "http://10.2.42.10:8088/lsystem"

payload = "idnum=pil-25-1942&library=LIB-PILI&Section=Second%20Floor"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, headers=headers, data=payload)

print(response.text)
