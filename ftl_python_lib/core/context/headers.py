from typing import Dict
from typing import Optional


class HeadersContext:
    def __init__(self, headers: Dict[str, str]) -> None:
        self.__headers = headers

    def to_dict(self) -> dict:
        """
        Class convertor to dict
        """

        return {
            "headers": self.__headers,
        }

    @property
    def request_headers(self) -> Optional[Dict[str, str]]:
        result: Dict[str, str] = {}

        for key, val in self.__headers.items():
            if "X-Transaction" in key or "x-transaction" in key:
                result[key] = val

        return result

    @property
    def content_type(self) -> Optional[str]:
        return self.__headers.get("Content-Type")

    @property
    def transaction_id(self) -> Optional[str]:
        return self.__headers.get("X-Transaction-Id")

    @property
    def mapping_type(self) -> Optional[str]:
        return self.__headers.get("X-Transaction-Mapping-Type")

    @property
    def mapping_source(self) -> Optional[str]:
        return self.__headers.get("X-Transaction-Mapping-Source")

    @property
    def mapping_target(self) -> Optional[str]:
        return self.__headers.get("X-Transaction-Mapping-Target")

    @property
    def mapping_message_type(self) -> Optional[str]:
        return self.__headers.get("X-Transaction-Mapping-Message-Type")

    @property
    def mapping_content_type(self) -> Optional[str]:
        return self.__headers.get("X-Transaction-Mapping-Content-Type")
