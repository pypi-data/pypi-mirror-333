import os
import sqlite3

from .exception import ToastNotificationsDBNotExist


class FetchToastPayload(object):
    _WPNDATABASE_PATH = os.path.expanduser(f"C:\\Users\\{os.environ.get('USERNAME')}\\AppData\\Local\\Microsoft\\Windows\\Notifications\\wpndatabase.db")

    def __init__(self, wpndatabase_path=None):
        self._wpndatabase = wpndatabase_path or self._WPNDATABASE_PATH
        self.check_wpndatabase_path()

        conn = sqlite3.connect(self._wpndatabase)
        self.cursor = conn.cursor()

    def check_wpndatabase_path(self):
        if not os.path.exists(self._wpndatabase):
            raise ToastNotificationsDBNotExist("Toast Notification Database does not exist.")

    def get_payload(self, trace_id) -> str:
        if not trace_id:
            return ""
        params = ("toast", trace_id)
        query = "SELECT `Payload` FROM `Notification` WHERE `Type` = ? AND `Id` = ?"

        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        payload = ""
        if result:
            payload = self.decoding_payload(result[0])
        return payload

    def decoding_payload(self, payload) -> str:
        return payload.decode("utf-8")
