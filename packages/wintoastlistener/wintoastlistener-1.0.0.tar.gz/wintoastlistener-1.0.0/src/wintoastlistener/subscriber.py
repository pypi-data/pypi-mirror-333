import base64
import os.path
from typing import Callable, Union
from urllib.parse import urlparse

import win32event
import win32evtlog

from .exception import ToastParserException, ToastEvtSubscribeActionError, ToastEvtSubscribeActionUnknown
from .fetch_toast_payload import FetchToastPayload
from .utils import parse_windows_event, parse_toast_raw_payload, parse_core_windows_event


class ToastListener(object):
    _EVENT_LOG_CHANNEL = "Microsoft-Windows-PushNotification-Platform/Operational"

    def __init__(
            self, callback: Callable[[dict, dict], None],
            app_id: str = '*',
            fetch_toast_content: bool = True,
            wpndatabase_path: str = None,
    ):
        """
        ToastListener Core
        :param callback: 监听回调函数
        """
        self._evt_flags = None
        self._evt_sub_handle = None
        self._roll_signal_handle = None

        self.app_id = app_id
        self.callback = callback
        self.fetch_toast_content = fetch_toast_content
        self._wpndatabase_path = wpndatabase_path

    def _parse_core_windows_event(self, event_data: str):
        return parse_core_windows_event(event_data)

    def _parse_windows_event(self, event_data: str):
        return parse_windows_event(event_data)

    def _event_filter(self, data: dict) -> bool:
        app_id = data.get("AppUserModelId")
        if not app_id:
            return False

        if self.app_id == '*':
            return True
        elif self.app_id == app_id:
            return True
        else:
            return False

    def _callback(self, action, user_context, event_handle):
        """
        事件触发回调
        :param action: 回调动作
        :param user_context: 用户上下文
        :param event_handle: 事件句柄
        :return: None
        """
        wpndb: Union[FetchToastPayload | None]
        wpndb = None
        if self.fetch_toast_content:
            wpndb = FetchToastPayload(wpndatabase_path=self._wpndatabase_path)
        if action == win32evtlog.EvtSubscribeActionDeliver:
            event_data = win32evtlog.EvtRender(event_handle, win32evtlog.EvtRenderEventXml)
            try:
                core_event_data = self._parse_core_windows_event(event_data)
                event_data = self._parse_windows_event(event_data)
            except Exception as e:
                raise ToastParserException(f"Toast xml parser exception - [{e}]")
            filter_status = self._event_filter(core_event_data)
            if filter_status:
                json_payload = {}
                if self.fetch_toast_content:
                    toast_raw_content = self._get_toast_payload(core_event_data, wpndb)
                    json_payload = self._parse_toast_payload(toast_raw_content)
                    self._extract_resource_file(json_payload)
                self.callback(event_data, json_payload)

        elif action == win32evtlog.EvtSubscribeActionError:
            raise ToastEvtSubscribeActionError(f"Subscribe Action Error - [{action}] - [{event_handle}]")
        else:
            raise ToastEvtSubscribeActionUnknown(f"Subscribe Action Unknown - [{action}] - [{event_handle}]")

    def listen(self, roll_cycle=500):
        user_context = None
        self._evt_flags = win32evtlog.EvtSubscribeToFutureEvents  # 订阅新日志
        self._evt_sub_handle = win32evtlog.EvtSubscribe(self._EVENT_LOG_CHANNEL, self._evt_flags, None, self._callback, user_context)

        self._roll_signal_handle = win32event.CreateEvent(None, False, False, None)

        while True:
            status = win32event.WaitForSingleObject(self._roll_signal_handle, roll_cycle)
            if status == win32event.WAIT_OBJECT_0:
                break

    def unlisten(self):
        self._evt_sub_handle.Close()
        win32event.SetEvent(self._roll_signal_handle)

    def _get_toast_payload(self, json_data: dict, wpndb) -> str:
        trace_id = json_data.get("TrackingId")
        if wpndb:
            return wpndb.get_payload(trace_id)
        return ""

    def _parse_toast_payload(self, toast_row_payload: str) -> dict:
        if toast_row_payload:
            result = parse_toast_raw_payload(toast_row_payload)
            return result
        else:
            return {}

    def _is_local_path(self, path: str) -> bool:
        return os.path.isabs(path) or os.path.exists(path)

    def _is_url_path(self, path: str) -> bool:
        parsed = urlparse(path)
        return bool(parsed.scheme and parsed.netloc)

    def _extract_and_write_resource_file(self, image_info: dict):
        image_src = image_info.get("@src", '')
        if self._is_local_path(image_src):
            with open(image_src, "rb") as image_file:
                base64_img = base64.b64encode(image_file.read()).decode()
            image_info["@src"] = base64_img
            image_info["img_type"] = "base64"
        elif self._is_url_path(image_src):
            image_info["img_type"] = "url"
        else:
            image_info["img_type"] = "other"

    def _extract_local_image(self, image_obj):
        if isinstance(image_obj, list):
            for image_info in image_obj:
                self._extract_and_write_resource_file(image_info)
        elif isinstance(image_obj, dict):
            self._extract_and_write_resource_file(image_obj)

    def _extract_resource_file(self, json_payload: dict) -> None:
        """递归解析"""
        for k, v in json_payload.items():
            if k == "image":
                self._extract_local_image(v)
            if isinstance(v, dict):
                self._extract_resource_file(v)
            else:
                continue
