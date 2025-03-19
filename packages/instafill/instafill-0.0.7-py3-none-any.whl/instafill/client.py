import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://api.instafill.ai/v1/forms"
SESSION_URL = "https://api.instafill.ai/v1/session"
PROFILE_URL = "https://api.instafill.ai/api/profile"

class InstaFillClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("INSTAFILL_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or in the .env file")

    def create_form(self, data, content_type="application/json"):
        headers = {"Content-Type": content_type, "x-api-key": self.api_key}
        if content_type == "application/json":
            response = requests.post(BASE_URL, headers=headers, json=data)
        elif content_type == "application/octet-stream":
            response = requests.post(BASE_URL, headers=headers, data=data)
        else:
            raise ValueError("Unsupported content type")
        response.raise_for_status()
        return response.json()

    def get_form(self, form_id):
        url = f"{BASE_URL}/{form_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def list_forms(self):
        headers = {"x-api-key": self.api_key}
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_form(self, form_id, data):
        url = f"{BASE_URL}/{form_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_session(self, data):
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        response = requests.post(SESSION_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_session(self, session_id):
        url = f"{SESSION_URL}/{session_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_profiles(self, name="", page=1, size=10, status=""):
        params = {
            "name": name,
            "page": page,
            "size": size,
            "status": status
        }
        headers = {"x-api-key": self.api_key}
        response = requests.get(PROFILE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def create_profile(self):
        headers = {"x-api-key": self.api_key}
        response = requests.get(f"{PROFILE_URL}/new", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_profile(self, profile_id):
        url = f"{PROFILE_URL}/{profile_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete_profile(self, profile_id):
        url = f"{PROFILE_URL}/{profile_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_profile_name(self, profile_id, name):
        url = f"{PROFILE_URL}/{profile_id}/name"
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        data = {"name": name}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def upload_files(self, profile_id, files):
        url = f"{PROFILE_URL}/{profile_id}/files"
        headers = {"x-api-key": self.api_key}
        files_data = [("files", (file.filename, file.file, file.content_type)) for file in files]
        response = requests.put(url, headers=headers, files=files_data)
        response.raise_for_status()
        return response.json()

    def delete_files(self, profile_id, file_ids):
        url = f"{PROFILE_URL}/{profile_id}/files"
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        data = {"ids": file_ids}
        response = requests.delete(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_profile_text_info(self, profile_id, text_info):
        url = f"{PROFILE_URL}/{profile_id}/text"
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        data = {"text_info": text_info}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
