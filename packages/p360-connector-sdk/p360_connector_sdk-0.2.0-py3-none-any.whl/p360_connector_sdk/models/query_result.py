from pydantic import BaseModel
from typing import Optional

from p360_connector_sdk.models.status import Status
from p360_connector_sdk.models.external_response import ExternalResponse


class QueryResult(BaseModel):
    """
    A model representing the result to a query request.

    Attributes:
        request_id (str): A unique identifier for the query request.
        turn_id (str): The unique identifier of the turn.
        session_id (str): The unique identifier of the session.
        tenant_id (str): The unique identifier of the tenant.
        response (ExternalResponse): The external response containing status, headers, and payload.
        status (Status): The connector processing status containing status code, and description.
    """

    request_id: str
    turn_id: str
    session_id: str
    tenant_id: str

    response: Optional[ExternalResponse] = None
    status: Status
