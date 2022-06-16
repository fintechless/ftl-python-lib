"""Create records related to one another via SQLAlchemy's ORM."""

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.models_helper.history_transaction import HelperHistoryTransaction
from ftl_python_lib.models_helper.message import HelperMessage
from ftl_python_lib.models_helper.microservice import HelperMicroservice
from ftl_python_lib.models_helper.transaction import HelperTransaction


class HelperDashboard:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Dashboard")

        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__history_transaction_helper: HelperHistoryTransaction = (
            HelperHistoryTransaction(
                request_context=self.__request_context,
                environ_context=self.__environ_context,
            )
        )

    def get_static_info(self):
        message_helper = HelperMessage(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        transaction_helper = HelperTransaction(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        microservice_helper = HelperMicroservice(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )

        response = {
            "message": {
                "total": len(message_helper.get_all()),
                "filtered": len(message_helper.get_all_active()),
            },
            "transaction": {
                "total": transaction_helper.count(),
                "filtered": transaction_helper.count_active(),
                "last_executed": [],
                "last_rejected": [],
            },
            "microservice": {
                "total": microservice_helper.count(),
                "filtered": microservice_helper.count_active(),
            },
            "rejection": {
                "total": self.__history_transaction_helper.get_total_volume(),
                "filtered": self.__history_transaction_helper.get_total_volume_rejected(),
            },
        }

        for item in self.__history_transaction_helper.get_last_execution():
            response["transaction"]["last_executed"].append(
                {"requested_at": item[0], "message_type": item[1], "status": item[2]}
            )
        for item in self.__history_transaction_helper.get_last_rejection():
            response["transaction"]["last_rejected"].append(
                {
                    "requested_at": item[0],
                    "message_type": item[1],
                    "response_code": item[2],
                    "response_message": item[3],
                    "description": item[4],
                }
            )

        return response

    def get_dynamic_info(self, from_date: str, to_date: str):
        transaction_volume_accepted = (
            self.__history_transaction_helper.get_volume_accepted(from_date, to_date)
        )
        transaction_volume_rejected = (
            self.__history_transaction_helper.get_volume_rejected(from_date, to_date)
        )
        transaction_volume_total = (
            transaction_volume_accepted + transaction_volume_rejected
        )

        transaction_currency_accepted = (
            self.__history_transaction_helper.get_currency_accepted(from_date, to_date)
        )
        transaction_currency_rejected = (
            self.__history_transaction_helper.get_currency_rejected(from_date, to_date)
        )
        transaction_currency_total = (
            transaction_currency_accepted + transaction_currency_rejected
        )

        response = {
            "transaction": {
                "volume": {
                    "total": transaction_volume_total,
                    "accepted": transaction_volume_accepted,
                    "accepted_percent": (
                        round(
                            transaction_volume_accepted
                            * 100
                            / transaction_volume_total,
                            2,
                        )
                        if transaction_volume_total > 0
                        else 0
                    ),
                    "rejected": transaction_volume_rejected,
                    "rejected_percent": (
                        round(
                            transaction_volume_rejected
                            * 100
                            / transaction_volume_total,
                            2,
                        )
                        if transaction_volume_total > 0
                        else 0
                    ),
                    "graph": [],
                },
                "currency": {
                    "total": transaction_currency_total,
                    "accepted": transaction_currency_accepted,
                    "accepted_percent": (
                        round(
                            transaction_currency_accepted
                            * 100
                            / transaction_currency_total,
                            2,
                        )
                        if transaction_currency_total > 0
                        else 0
                    ),
                    "rejected": transaction_currency_rejected,
                    "rejected_percent": (
                        round(
                            transaction_currency_rejected
                            * 100
                            / transaction_currency_total,
                            2,
                        )
                        if transaction_currency_total > 0
                        else 0
                    ),
                    "graph": [],
                },
            },
        }

        self._get_volume_graph(from_date, to_date, response)
        self._get_currency_graph(from_date, to_date, response)

        return response

    def _get_volume_graph(self, from_date, to_date, response):
        filter_by_time = []
        if from_date[0:10] == to_date[0:10]:
            filter_by_time = self.__history_transaction_helper.get_volume_by_hour(
                from_date, to_date
            )
        else:
            filter_by_time = self.__history_transaction_helper.get_volume_by_day(
                from_date, to_date
            )

        response["transaction"]["volume"]["graph"] = self._get_graph(filter_by_time)

    def _get_currency_graph(self, from_date, to_date, response):
        filter_by_time = []
        if from_date[0:10] == to_date[0:10]:
            filter_by_time = self.__history_transaction_helper.get_currency_by_hour(
                from_date, to_date
            )
        else:
            filter_by_time = self.__history_transaction_helper.get_currency_by_day(
                from_date, to_date
            )
        response["transaction"]["currency"]["graph"] = self._get_graph(filter_by_time)

    def _get_graph(self, filter_by_time):
        graph_map = {}
        for item in filter_by_time:
            time_key = str(item[0])
            status_key = "accepted" if item[1] == "RELEASED" else "rejected"
            if time_key not in graph_map:
                graph_map[time_key] = {}
            if status_key not in graph_map[time_key]:
                graph_map[time_key][status_key] = {}
            graph_map[time_key][status_key] = item[2]

        graph = []
        for key, value in graph_map.items():
            graph.append(
                {
                    "timeData": key,
                    "accepted": value["accepted"] if "accepted" in value.keys() else 0,
                    "rejected": value["rejected"] if "rejected" in value.keys() else 0,
                }
            )
        return graph
