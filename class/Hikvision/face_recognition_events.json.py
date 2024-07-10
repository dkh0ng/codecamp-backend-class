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

def fetch_door_list():
    url = '/artemis/api/resource/v1/acsDevice/acsDeviceList'
    full_url = BASE_URL + url
    headers = get_headers()

    body = json.dumps({
        "pageNo": 1,
        "pageSize": 100
    })
    headers['Content-MD5'] = base64.b64encode(hashlib.md5(body.encode('utf-8')).digest()).decode('utf-8')
    headers['x-ca-signature-headers'] = 'x-ca-key,x-ca-timestamp'
    headers['x-ca-signature'] = get_signature('POST', url, headers, body)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.post(full_url, headers=headers, data=body, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def fetch_region_list():
    url = '/artemis/api/resource/v1/regions'
    full_url = BASE_URL + url
    headers = get_headers()

    body = json.dumps({
        "pageNo": 1,
        "pageSize": 10
    })
    headers['Content-MD5'] = base64.b64encode(hashlib.md5(body.encode('utf-8')).digest()).decode('utf-8')
    headers['x-ca-signature-headers'] = 'x-ca-key,x-ca-timestamp'
    headers['x-ca-signature'] = get_signature('POST', url, headers, body)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.post(full_url, headers=headers, data=body, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def fetch_face_recognition_events(door_list_index, region_index):
    url = '/artemis/api/aiapplication/v1/face/faceMatchRecord'
    full_url = BASE_URL + url
    headers = get_headers()

    seoul_time = datetime.now(timezone.utc) + timedelta(hours=9)
    start_time = seoul_time - timedelta(days=7)  # 시작 시간: 현재 시간으로부터 7일 전
    end_time = seoul_time  # 종료 시간: 현재 시간

    body = json.dumps({
        "pageNo": 1,
        "pageSize": 100,  # 페이지 크기를 100으로 설정
        "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "endTime": end_time.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "cameraIndexCodes": ["1", "2", "3"],  # 예시 카메라 인덱스 코드; 실제 값으로 변경
        "personIndexCodes": [],  # 필요한 경우 인물 인덱스 추가
        "doorListIndex": door_list_index,  # 도어 인덱스 리스트
        "regionIndex": region_index  # 리전 인덱스
    })
    headers['Content-MD5'] = base64.b64encode(hashlib.md5(body.encode('utf-8')).digest()).decode('utf-8')
    headers['x-ca-signature-headers'] = 'x-ca-key,x-ca-timestamp'
    headers['x-ca-signature'] = get_signature('POST', url, headers, body)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.post(full_url, headers=headers, data=body, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    doors = fetch_door_list()
    if not doors:
        print("Failed to fetch door list.")
        exit(1)

    regions = fetch_region_list()
    if not regions:
        print("Failed to fetch region list.")
        exit(1)
        
    door_list_index = [door['acsDevIndexCode'] for door in doors['data']['list']]
    region_index = regions['data']['list'][0]['indexCode']  # 예시로 첫 번째 지역 사용

    records = fetch_face_recognition_events(door_list_index, region_index)
    if records:
        with open(r'C:\Users\eden_clo3d\Desktop\face_recognition_events.json', 'w') as f:
            json.dump(records, f, indent=4)
        print("JSON file has been saved to C:\\Users\\eden_clo3d\\Desktop\\face_recognition_events.json")
    else:
        print("Failed to fetch face recognition events.")
