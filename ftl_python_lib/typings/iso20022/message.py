"""
Custom typing for ISO20022 message
"""


class TypeMessage(dict):
    """
    Custom typing for ISO20022 message
    """

    @property
    def message_type(self) -> str:
        """
        Get message_type value
        """

        return self.get("Document").get("@xmlns").split(":").pop()

    @property
    def creditor_name(self) -> str:
        """
        Get creditor's name
        """

        return (
            self.get("Document")
            .get("FIToFICstmrCdtTrf")
            .get("CdtTrfTxInf")
            .get("Cdtr")
            .get("Nm")
        )

    @property
    def creditor_account(self) -> str:
        """
        Get creditor's account
        """

        return (
            self.get("Document")
            .get("FIToFICstmrCdtTrf")
            .get("CdtTrfTxInf")
            .get("CdtrAcct")
            .get("Id")
            .get("Othr")
            .get("Id")
        )

    @property
    def debitor_name(self) -> str:
        """
        Get debitor's name
        """

        return (
            self.get("Document")
            .get("FIToFICstmrCdtTrf")
            .get("CdtTrfTxInf")
            .get("Dbtr")
            .get("Nm")
        )

    @property
    def debitor_account(self) -> str:
        """
        Get debitor's account
        """

        return (
            self.get("Document")
            .get("FIToFICstmrCdtTrf")
            .get("CdtTrfTxInf")
            .get("DbtrAcct")
            .get("Id")
            .get("Othr")
            .get("Id")
        )

    @property
    def amount(self) -> int:
        """
        Get transfer amount
        """

        return int(
            self.get("Document")
            .get("FIToFICstmrCdtTrf")
            .get("CdtTrfTxInf")
            .get("IntrBkSttlmAmt")
            .get("#text")
        )

    @property
    def currency(self) -> str:
        """
        Get transfer currency
        """

        return (
            self.get("Document")
            .get("FIToFICstmrCdtTrf")
            .get("CdtTrfTxInf")
            .get("IntrBkSttlmAmt")
            .get("@Ccy")
        )
