import mimetypes


def mime_json() -> str:
    return mimetypes.types_map.get(".json")


def mime_xml() -> str:
    return mimetypes.types_map.get(".xml")


def mime_is_xml(mime: str) -> bool:
    if mime in (mimetypes.types_map.get(".xml", "text/xml"), "application/xml"):
        return True

    return False


def mime_is_json(mime: str) -> bool:
    if mime in (mimetypes.types_map.get(".json", "application/json")):
        return True

    return False
