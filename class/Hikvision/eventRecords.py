import requests
import hashlib
import hmac
import base64
import time
import uuid
import json
import urllib3
from datetime import datetime, timedelta, timezone

# Provided authentication information
APPkey = '28757503'
APPsecret = 'DuRmSZPTSZlMymDz2gon'
BASE_URL = 'https://192.168.29.74'

def get_signature(http_method, url, headers, body=''):
    content_md5 = hashlib.md5(body.encode('utf-8')).digest()
    content_md5_base64 = base64.b64encode(content_md5).decode('utf-8')

    string_to_sign = f"{http_method}\n*/*\n{content_md5_base64}\napplication/json\n{headers['Date']}\n"
    string_to_sign += f"x-ca-key:{headers['x-ca-key']}\n"
    string_to_sign += f"x-ca-timestamp:{headers['x-ca-timestamp']}\n"
    string_to_sign += url

    signature = hmac.new(APPsecret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

def get_headers():
    headers = {
        'Accept': '*/*',
        'Content-MD5': '',
        'Content-Type': 'application/json',
        'Date': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()),
        'x-ca-key': APPkey,
        'x-ca-timestamp': str(int(time.time() * 1000)),
        'x-ca-nonce': str(uuid.uuid4())
    }
    return headers

def fetch_event_records():
    url = '/artemis/api/eventService/v1/eventRecords/page'
    full_url = BASE_URL + url
    headers = get_headers()

    body = json.dumps({
        "pageNo": 1,
        "pageSize": 100,
        "startTime": "2024-07-01T00:00:00+09:00",
        "endTime": "2024-07-11T23:59:59+09:00",
        "eventTypes": "196609",  # 얼굴 인증 성공 이벤트 타입 코드
        "srcType": "camera",
        "srcIndexs": "1,2",
        "subSrcType": "LPRVehicleList",
        "subSrcIndexs": "1,2,3,4",
        "sortField": "TriggeringTime",
        "orderType": 1
    })
    headers['Content-MD5'] = base64.b64encode(hashlib.md5(body.encode('utf-8')).digest()).decode('utf-8')
    headers['x-ca-signature-headers'] = 'x-ca-key,x-ca-timestamp'
    headers['x-ca-signature'] = get_signature('POST', url, headers, body)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.post(full_url, headers=headers, data=body, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching event records: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    event_records = fetch_event_records()
    if event_records:
        with open(r'C:\Users\eden_clo3d\Desktop\event_records.json', 'w') as f:
            json.dump(event_records, f, indent=4)
        print("JSON file has been saved to C:\\Users\\eden_clo3d\\Desktop\\event_records.json")
    else:
        print("Failed to fetch event records.")
