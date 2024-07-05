from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import time
import logging

# 설정
SERVICE_ACCOUNT_FILE = 'clo-developer-3a3da4a55859.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 서비스 계정 인증
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# 업로드할 파일 경로와 Google Drive 폴더 ID 설정
LOCAL_FILE_PATH = r'C:\Users\eden_clo3d\Desktop\asdf.zip'
DRIVE_FOLDER_ID = '0AP_3h1WEDE--Uk9PVA' 

def check_folder_access():
    try:
        folder = service.files().get(fileId=DRIVE_FOLDER_ID, supportsAllDrives=True).execute()
        print(f"Folder '{folder['name']}' exists and is accessible.")
    except Exception as e:
        print(f"Error accessing folder: {e}")

def upload_file():
    logger.info('Script started by user: %s', os.getenv('USERNAME'))
    file_size = os.path.getsize(LOCAL_FILE_PATH)
    logger.info(f'Uploading file of size: {file_size} bytes')

    file_metadata = {
        'name': os.path.basename(LOCAL_FILE_PATH),
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(LOCAL_FILE_PATH, mimetype='application/octet-stream', resumable=True)
    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%.")
                logger.info(f"Uploaded {int(status.progress() * 100)}%.")
        except Exception as e:
            print(f'Error: {e}')
            logger.error(f'Error: {e}', exc_info=True)
            time.sleep(5)  # 5초 대기 후 재시도

    print(f'File ID: {response.get("id")}')
    logger.info(f'File ID: {response.get("id")}')

if __name__ == '__main__':
    check_folder_access()
    upload_file()
