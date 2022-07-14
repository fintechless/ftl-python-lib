import os
from typing import Optional

from ftl_python_lib.utils.mime import mime_is_json
from ftl_python_lib.utils.mime import mime_is_xml
from ftl_python_lib.utils.timedate import DateTime
from ftl_python_lib.utils.timezone import get_timezone


def storage_key(
    transaction_id: str,
    incoming: bool,
    message_version: Optional[str],
    requested_at: DateTime,
    content_type: str,
) -> str:
    """
    :param incoming: Destination folder in S3
    :type incoming: bool
    :param message_type: Type of the XML message
    :type message_type: str
    """

    def round_microseconds(micros: int) -> int:
        return int(round(micros, -3) / 1000)

    microsecond: str = str(round_microseconds(micros=requested_at.microsecond))
    timezone: str = get_timezone()
    in_out: str = "in" if incoming is True else "out"
    ext: str = "xml" if mime_is_xml(mime=content_type) else "json"

    if message_version is None:
        key: str = os.path.join(
            in_out,
            str(requested_at.year),
            str(requested_at.month).zfill(2),
            str(requested_at.day).zfill(2),
            str(requested_at.hour).zfill(2),
            str(requested_at.minute).zfill(2),
            str(requested_at.second).zfill(2),
            f"{microsecond}{timezone}",
            f"{transaction_id}.{ext}",
        )
    else:
        key: str = os.path.join(
            in_out,
            str(requested_at.year),
            str(requested_at.month).zfill(2),
            str(requested_at.day).zfill(2),
            str(requested_at.hour).zfill(2),
            str(requested_at.minute).zfill(2),
            str(requested_at.second).zfill(2),
            f"{microsecond}{timezone}",
            f"{transaction_id}-{message_version}.{ext}",
        )

    return key
