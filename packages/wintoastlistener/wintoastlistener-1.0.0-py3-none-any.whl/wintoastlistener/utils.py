from xml.etree import ElementTree

import xmltodict


def parse_core_windows_event(xml_string):
    namespace = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    root = ElementTree.fromstring(xml_string)
    core_event_data = {}

    for data in root.findall(".//ns:EventData/ns:Data", namespace):
        name = data.attrib.get("Name", "Unknown")
        if name == "AppUserModelId" or name == "TrackingId":
            core_event_data[name] = data.text if data.text else ""
    return core_event_data


def parse_windows_event(xml_string):
    result = xmltodict.parse(xml_string)
    return result.get("Event", {})


def parse_toast_raw_payload(xml_string):
    result = xmltodict.parse(xml_string)
    return result.get("toast", {})
