from enum import Enum
from enum import EnumMeta


class ConstantsMessagesAllowReleaseMeta(EnumMeta):
    def __contains__(self, item):
        try:
            self(item)
        except ValueError:
            return False
        else:
            return True


class ConstantsMessagesAllowRelease(Enum, metaclass=ConstantsMessagesAllowReleaseMeta):
    PACS_008 = "pacs.008"


class ConstantsMessagesTypes(Enum):
    PACS_002 = "pacs.002"
    PACS_008 = "pacs.008"
