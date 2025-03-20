import requests
import json

class SafeW:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.safew.org/bot{token}/"

    def _request(self, method: str, params: dict = None, files: dict = None):
        url = self.base_url + method
        response = requests.post(url, data=params, files=files) if files else requests.get(url, params=params)
        return response.json()

    def getMe(self):
        return self._request("getMe")

    def sendMessage(self, chat_id: int, text: str, parse_mode: str = "Markdown", reply_markup: dict = None):
        params = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        return self._request("sendMessage", params)

    def sendVideo(self, chat_id: int, video: str, caption: str = "", parse_mode: str = "Markdown"):
        with open(video, "rb") as file:
            return self._request("sendVideo", {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}, {"video": file})

    def getChatMemberCount(self, chat_id: int):
        return self._request("getChatMemberCount", {"chat_id": chat_id})

    def getUpdates(self, offset: int = None, limit: int = 100):
        params = {"limit": limit}
        if offset:
            params["offset"] = offset
        return self._request("getUpdates", params)

    def editMessageText(self, chat_id: int, message_id: int, text: str, parse_mode: str = "Markdown", reply_markup: dict = None):
        params = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        return self._request("editMessageText", params)

    def forwardMessage(self, chat_id: int, from_chat_id: int, message_id: int):
        params = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id}
        return self._request("forwardMessage", params)