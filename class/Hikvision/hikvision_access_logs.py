from dotenv import load_dotenv
import os
import requests
import json

# 환경 변수 로드
load_dotenv()

print("환경 변수 로드 완료")

# Hikvision API URL 및 인증 정보
api_base_url = f"http://{os.getenv('HIKVISION_SERVER_IP')}:{os.getenv('PORT')}"
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

print("API URL 및 인증 정보 설정 완료")

# 인증 토큰 받기
def get_token():
    try:
        login_url = f'{api_base_url}/api/v1/auth/login'
        print(f"로그인 URL: {login_url}")
        response = requests.post(login_url, json={'username': username, 'password': password})
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        response_data = response.json()
        print("토큰 받기 성공")
        return response_data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"토큰 받기 에러: {e}")
        return None

# 출입 기록 가져오기
def get_access_logs(token):
    if token is None:
        print("토큰이 None, 출입 기록 가져올 수 없음")
        return {}
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        access_logs_url = f'{api_base_url}/api/v1/entranceGuard/attendanceRecord/search'
        print(f"출입 기록 URL: {access_logs_url}")
        response = requests.post(access_logs_url, headers=headers, json={})
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        print("출입 기록 가져오기 성공")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"출입 기록 가져오기 에러: {e}")
        return {}

print("토큰 받기 시도 중")
# 토큰 가져오기
token = get_token()

print("출입 기록 가져오기 시도 중")
# 출입 기록 가져오기
access_logs = get_access_logs(token)

print("출입 기록 출력")
# 결과 출력 (혹은 필요한 로직 처리)
print(json.dumps(access_logs, indent=4))

print("출입 기록 파일에 저장 중")
# 출입 기록을 파일에 저장
with open('access_logs.json', 'w') as file:
    json.dump(access_logs, file, indent=4)
print("출입 기록 파일에 저장 완료")
