import json
from typing import Dict
from typing import List
from typing import Union

from ftl_python_lib.constants.models.mapping import ConstantsMappingInFailedOut
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.providers.aws.s3 import ProviderS3
from ftl_python_lib.typings.providers.aws.s3object import TypeS3Object
from ftl_python_lib.utils.mime import mime_is_json
from ftl_python_lib.utils.mime import mime_is_xml
from ftl_python_lib.utils.xml.processing import parse as xml_parse
from ftl_python_lib.utils.xml.processing import unparse as xml_unparse
from ftl_python_lib.utils.xml.storage import storage_key
from ftl_python_lib.utils.to_str import bytes_to_str


class TypeReceivedMessageVersionKeys:
    def __init__(
        self,
        unique_type: str,
        version_major: str,
        version_minor: str,
        version_patch: str,
    ) -> None:
        self.__unique_type = unique_type
        self.__version_major = version_major
        self.__version_minor = version_minor
        self.__version_patch = version_patch

    @property
    def unique_type(self) -> str:
        return self.__unique_type

    @property
    def version_major(self) -> str:
        return self.__version_major

    @property
    def version_minor(self) -> str:
        return self.__version_minor

    @property
    def version_patch(self) -> str:
        return self.__version_patch


class TypeReceivedMessageProc:
    __message_type = None
    __message_version = None
    __storage_path = None
    __message_version_keys = None

    __xml = None
    __proc = None

    def __init__(
        self,
        message_proc: Union[Dict[str, str], dict],
        request_context: RequestContext,
        environ_context: EnvironmentContext,
    ) -> None:
        if message_proc is None:
            raise ValueError("Processed message content must not be NoneType")
        self.__message_proc = message_proc
        self.__request_context = request_context
        self.__environ_context = environ_context

    def to_xml(self) -> str:
        if self.__xml is not None:
            return self.__xml

        self.__xml = xml_unparse(src=self.__message_proc)

        return self.__xml

    def to_dict(self) -> str:
        if self.__proc is not None:
            return self.__proc

        self.__proc = self.__message_proc

        return self.__proc

    def fill_message_type(self) -> None:
        try:
            self.__message_type = ".".join(
                self.__message_proc.get("Document")
                .get("@xmlns")
                .split(":")
                .pop()
                .split(".")[:2]
            )
        except Exception as exception:
            raise ValueError(
                f"Could not retrieve 'message_type' from 'message_proc' due to invalid message: {exception}"
            ) from exception

    def fill_message_version(self) -> None:
        try:
            self.__message_version = (
                self.__message_proc.get("Document").get("@xmlns").split(":").pop()
            )
        except Exception as exception:
            raise ValueError(
                f"Could not retrieve 'message_version' from 'message_proc' due to invalid message: {exception}"
            ) from exception

    def fill_message_version_keys(self) -> None:
        def getval(src: List[str], index: int):
            try:
                return src[index]
            except IndexError:
                return None

        if self.__message_version_keys is not None:
            return
        version_split: List[str] = self.__message_version.split(".")
        self.__message_version_keys = TypeReceivedMessageVersionKeys(
            unique_type=getval(src=version_split, index=0),
            version_major=getval(src=version_split, index=1),
            version_minor=getval(src=version_split, index=2),
            version_patch=getval(src=version_split, index=3),
        )

    # def upload_to_storage(self, incoming: bool):
    #     storage_provider: ProviderS3 = ProviderS3(
    #         request_context=self.__request_context,
    #         environ_context=self.__environ_context,
    #     )
    #     key: str = storage_key(
    #         transaction_id=self.__request_context.transaction_id,
    #         incoming=incoming,
    #         message_version=self.__message_version,
    #         requested_at=self.__request_context.requested_at_datetime,
    #     )

    #     self.__storage_path = TypeS3Object(
    #         key=key,
    #         body=self.__message_proc,
    #         bucket=self.__environ_context.deploy_bucket,
    #     )

    #     storage_provider.put_object(object=self.__storage_path)

    @property
    def message_type(self) -> str:
        # Example: pacs.002
        return self.__message_type

    @property
    def message_version(self) -> str:
        # Example: pacs.002.001.01
        return self.__message_version

    @property
    def message_version_keys(self) -> TypeReceivedMessageVersionKeys:
        return self.__message_version_keys
    
    @property
    def creditor_name(self) -> str:
        """
        Get creditor's name
        """

        try:
            return (
                self.__message_proc.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("Cdtr")
                .get("Nm")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def creditor_account(self) -> str:
        """
        Get creditor's account
        """

        try:
            return (
                self.__message_proc.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("CdtrAcct")
                .get("Id")
                .get("Othr")
                .get("Id")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def debitor_name(self) -> str:
        """
        Get debitor's name
        """

        try:
            return (
                self.__message_proc.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("Dbtr")
                .get("Nm")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def debitor_account(self) -> str:
        """
        Get debitor's account
        """

        try:
            return (
                self.__message_proc.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("DbtrAcct")
                .get("Id")
                .get("Othr")
                .get("Id")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def amount(self) -> int:
        """
        Get transfer amount
        """

        try:
            amount: str = (
                self.__message_proc.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("IntrBkSttlmAmt")
                .get("#text")
            )

            if amount.isdigit():
                return int(amount)
            return 0
        except (ValueError, KeyError):
            return 0

    @property
    def currency(self) -> str:
        """
        Get transfer currency
        """

        try:
            return (
                self.__message_proc.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("IntrBkSttlmAmt")
                .get("@Ccy")
            )
        except (ValueError, KeyError):
            return "N/A"


class TypeReceivedMessageOut:
    __message_type = None
    __message_version = None
    __storage_path = None
    __message_version_keys = None

    __xml = None
    __out = None

    def __init__(
        self,
        message_out: Union[Dict[str, str], dict],
        request_context: RequestContext,
        environ_context: EnvironmentContext,
    ) -> None:
        if message_out is None:
            raise ValueError("Out message content must not be NoneType")
        self.__message_out = message_out
        self.__request_context = request_context
        self.__environ_context = environ_context

    def to_xml(self) -> str:
        if self.__xml is not None:
            return self.__xml

        self.__xml = xml_unparse(src=self.__message_out)

        return self.__xml

    def to_dict(self) -> str:
        if self.__out is not None:
            return self.__out

        self.__out = self.__message_out

        return self.__out

    def fill_message_type(self) -> None:
        try:
            self.__message_type = ".".join(
                self.__message_out.get("Document")
                .get("@xmlns")
                .split(":")
                .pop()
                .split(".")[:2]
            )
        except Exception as exception:
            raise ValueError(
                f"Could not retrieve 'message_type' from 'message_out' due to invalid message: {exception}"
            ) from exception

    def fill_message_version(self) -> None:
        try:
            self.__message_version = (
                self.__message_out.get("Document").get("@xmlns").split(":").pop()
            )
        except Exception as exception:
            raise ValueError(
                f"Could not retrieve 'message_version' from 'message_out' due to invalid message: {exception}"
            ) from exception

    def fill_message_version_keys(self) -> None:
        def getval(src: List[str], index: int):
            try:
                return src[index]
            except IndexError:
                return None

        if self.__message_version_keys is not None:
            return
        version_split: List[str] = self.__message_version.split(".")
        self.__message_version_keys = TypeReceivedMessageVersionKeys(
            unique_type=getval(src=version_split, index=0),
            version_major=getval(src=version_split, index=1),
            version_minor=getval(src=version_split, index=2),
            version_patch=getval(src=version_split, index=3),
        )

    # def upload_to_storage(self, incoming: bool):
    #     storage_provider: ProviderS3 = ProviderS3(
    #         request_context=self.__request_context,
    #         environ_context=self.__environ_context,
    #     )
    #     key: str = storage_key(
    #         transaction_id=self.__request_context.transaction_id,
    #         incoming=incoming,
    #         message_version=self.__message_version,
    #         requested_at=self.__request_context.requested_at_datetime,
    #     )

    #     self.__storage_path = TypeS3Object(
    #         key=key,
    #         body=self.__message_out,
    #         bucket=self.__environ_context.deploy_bucket,
    #     )

    #     storage_provider.put_object(object=self.__storage_path)

    @property
    def message_out(self) -> Union[Dict[str, str], dict]:
        return self.__message_out

    @property
    def message_type(self) -> str:
        # Example: pacs.002
        return self.__message_type

    @message_type.setter
    def message_type(self, message_type: str) -> None:
        self.__message_type = message_type

    @property
    def message_version(self) -> str:
        # Example: pacs.002.001.01
        return self.__message_version

    @message_version.setter
    def message_version(self, message_version: str) -> None:
        self.__message_version = message_version

    @property
    def message_version_keys(self) -> TypeReceivedMessageVersionKeys:
        return self.__message_version_keys

    @message_version_keys.setter
    def message_version_keys(
        self, message_version_keys: TypeReceivedMessageVersionKeys
    ) -> None:
        self.__message_version_keys = message_version_keys

    @property
    def creditor_name(self) -> str:
        """
        Get creditor's name
        """

        try:
            return (
                self.__message_out.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("Cdtr")
                .get("Nm")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def creditor_account(self) -> str:
        """
        Get creditor's account
        """

        try:
            return (
                self.__message_out.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("CdtrAcct")
                .get("Id")
                .get("Othr")
                .get("Id")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def debitor_name(self) -> str:
        """
        Get debitor's name
        """

        try:
            return (
                self.__message_out.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("Dbtr")
                .get("Nm")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def debitor_account(self) -> str:
        """
        Get debitor's account
        """

        try:
            return (
                self.__message_out.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("DbtrAcct")
                .get("Id")
                .get("Othr")
                .get("Id")
            )
        except (ValueError, KeyError):
            return "N/A"

    @property
    def amount(self) -> int:
        """
        Get transfer amount
        """

        try:
            amount: str = (
                self.__message_out.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("IntrBkSttlmAmt")
                .get("#text")
            )

            if amount.isdigit():
                return int(amount)
            return 0
        except (ValueError, KeyError):
            return 0

    @property
    def currency(self) -> str:
        """
        Get transfer currency
        """

        try:
            return (
                self.__message_out.get("Document")
                .get("FIToFICstmrCdtTrf")
                .get("CdtTrfTxInf")
                .get("IntrBkSttlmAmt")
                .get("@Ccy")
            )
        except (ValueError, KeyError):
            return "N/A"


class TypeReceivedMessage:
    __message_proc = None
    __message_out = None
    __message_xml = None
    __message_type = None
    __message_version = None
    __storage_path = None
    __message_version_keys = None

    def __init__(
        self,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
        message_raw: Union[Dict[str, str], str, bytes],
        content_type: str,
    ) -> None:
        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__content_type = content_type
        self.__message_raw = message_raw

    @property
    def request_id(self) -> str:
        return self.__request_context.request_id

    @property
    def requested_at(self) -> str:
        return self.__request_context.requested_at_isoformat

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def message_raw(self) -> Union[Dict[str, str], str, bytes]:
        return self.__message_raw

    @message_raw.setter
    def message_raw(self, message_raw: Union[Dict[str, str], str, bytes]) -> None:
        self.__message_raw = message_raw

    @property
    def message_xml(self) -> str:
        return self.__message_xml

    @message_xml.setter
    def message_rat(self, message_xml: str) -> None:
        self.__message_xml = message_xml

    @property
    def message_proc(self) -> TypeReceivedMessageProc:
        return self.__message_proc

    @message_proc.setter
    def message_proc(self, message_proc: TypeReceivedMessageProc) -> None:
        self.__message_proc = message_proc

    @property
    def message_out(self) -> Union[Dict[str, str], str, bytes]:
        return self.__message_out

    @property
    def message_type(self) -> str:
        # Example: pacs.008
        return self.__message_type

    @message_type.setter
    def message_type(self, message_type: str) -> None:
        self.__message_type = message_type

    @property
    def message_version(self) -> str:
        # Example: pacs.008.001.10
        return self.__message_version

    @message_version.setter
    def message_version(self, message_version: str) -> None:
        self.__message_version = message_version

    @property
    def message_version_keys(self) -> TypeReceivedMessageVersionKeys:
        return self.__message_version_keys

    @message_version_keys.setter
    def message_version_keys(
        self, message_version_keys: TypeReceivedMessageVersionKeys
    ) -> None:
        self.__message_version_keys = message_version_keys

    @property
    def message_type_out_failed(self) -> str:
        return ConstantsMappingInFailedOut.which(key=self.__message_type)

    @property
    def storage_path(self) -> TypeS3Object:
        return self.__storage_path

    @storage_path.setter
    def storage_path(self, storage_path: TypeS3Object) -> None:
        self.__storage_path = storage_path

    def fill_message_proc(self) -> None:
        if self.__message_proc is not None:
            return
        if mime_is_json(mime=self.__content_type) and isinstance(
            self.__message_raw, dict
        ):
            try:
                self.__message_proc = TypeReceivedMessageProc(
                    message_proc=self.__message_raw,
                    request_context=self.__request_context,
                    environ_context=self.__environ_context,
                )
                return
            except Exception as exception:
                raise ValueError(
                    f"Received invalid raw message: {exception}"
                ) from exception
        if mime_is_xml(mime=self.__content_type) and (
            isinstance(self.__message_raw, (str, bytes))
        ):
            try:
                self.__message_proc = TypeReceivedMessageProc(
                    message_proc=xml_parse(src=self.__message_raw),
                    request_context=self.__request_context,
                    environ_context=self.__environ_context,
                )
                return
            except Exception as exception:
                raise ValueError(
                    f"Received invalid raw message: {exception}"
                ) from exception
        raise ValueError(
            f"Received invalid Content-Type '{self.__content_type}'"
            + " and '{type(self.__message_raw)}' when preparing 'message_proc'"
        )

    def fill_message_xml(self) -> None:
        if self.__message_xml is not None:
            return
        if mime_is_json(mime=self.__content_type) and isinstance(
            self.__message_raw, dict
        ):
            try:
                self.__message_xml = xml_unparse(src=self.__message_raw)
                return
            except Exception as exception:
                raise ValueError(
                    f"Received invalid raw message: {exception}"
                ) from exception
        if mime_is_xml(mime=self.__content_type) and (
            isinstance(self.__message_raw, (str, bytes))
        ):
            try:
                self.__message_xml = self.__message_raw
                return
            except Exception as exception:
                raise ValueError(
                    f"Received invalid raw message: {exception}"
                ) from exception
        raise ValueError(
            f"Received invalid Content-Type '{self.__content_type}'"
            + " and '{type(self.__message_raw)}' when preparing 'message_xml'"
        )

    def fill_message_out(self) -> None:
        # Nothing to do here yet
        pass

    def fill_message_type(self) -> None:
        try:
            self.__message_type = ".".join(
                self.__message_proc.to_dict()
                .get("Document")
                .get("@xmlns")
                .split(":")
                .pop()
                .split(".")[:2]
            )
        except Exception as exception:
            raise ValueError(
                f"Could not retrieve 'message_type' from 'message_proc' due to invalid message: {exception}"
            ) from exception

    def fill_message_version(self, from_header: str = None) -> None:
        if from_header is not None:
            self.__message_version = from_header
            return
        try:
            self.__message_version = (
                self.__message_proc.to_dict()
                .get("Document")
                .get("@xmlns")
                .split(":")
                .pop()
            )
        except Exception:
            self.__message_version = None
            # raise ValueError(
            #     f"Could not retrieve 'message_version' from 'message_proc' due to invalid message: {exception}"
            # ) from exception

    def fill_message_version_keys(self) -> None:
        def getval(src: List[str], index: int):
            try:
                return src[index]
            except IndexError:
                return None

        if self.__message_version_keys is not None:
            return
        version_split: List[str] = self.__message_version.split(".")
        self.__message_version_keys = TypeReceivedMessageVersionKeys(
            unique_type=getval(src=version_split, index=0),
            version_major=getval(src=version_split, index=1),
            version_minor=getval(src=version_split, index=2),
            version_patch=getval(src=version_split, index=3),
        )

    def upload_to_storage(self, incoming: bool):
        storage_provider: ProviderS3 = ProviderS3(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        key: str = storage_key(
            transaction_id=self.__request_context.transaction_id,
            incoming=incoming,
            message_version=self.__message_version,
            requested_at=self.__request_context.requested_at_datetime,
            content_type=self.__content_type
        )

        self.__storage_path = TypeS3Object(
            key=key,
            body=self.__message_raw if isinstance(self.__message_raw, (str, bytes)) else json.dumps(bytes_to_str(src=self.__message_raw)),
            bucket=self.__environ_context.deploy_bucket,
        )

        storage_provider.put_object(object=self.__storage_path)
