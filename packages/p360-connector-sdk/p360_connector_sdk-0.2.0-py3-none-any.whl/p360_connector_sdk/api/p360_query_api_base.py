from abc import ABC, abstractmethod

from p360_connector_sdk.models.query_request import QueryRequest
from p360_connector_sdk.models.query_ack_response import QueryAcknowledgementResponse


class P360QueryAPIBase(ABC):
    """
    An abstract base class that defines the interface for a P360 query API.

    This class enforces the implementation of query method that accepts the query request
    and returns a corresponding acknowledgement immediately.
    Note:   After acknowledgement, the request will be processed asynchronously and
            the results are sent to P360 servers via a provided callback url with
            the response payload modeled as p360_connector_sdk.QueryResult

    Methods:
        query(request: QueryRequest) -> QueryAcknowledgementResponse:
            Abstract method to process a query request and return the acknowledgement response.
    """

    @abstractmethod
    def query(self, request: QueryRequest) -> QueryAcknowledgementResponse:
        """
        Process the query and return the acknowledgement response.
        
        Args:
            request (QueryRequest): The query request payload.
        
        Returns:
            QueryAcknowledgementResponse: The query acknowledgement response.
        """
