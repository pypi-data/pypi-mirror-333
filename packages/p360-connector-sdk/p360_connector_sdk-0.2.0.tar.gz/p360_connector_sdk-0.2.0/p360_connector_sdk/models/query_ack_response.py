from pydantic import BaseModel

from p360_connector_sdk.models.status import Status


class QueryAcknowledgementResponse(BaseModel):
    """
    A model representing the acknowledgement response to a query request.

    Attributes:
        request_id (str): A unique identifier for the request.
        turn_id (str): The unique identifier of the turn.
        session_id (str): The unique identifier of the session.
        tenant_id (str): The unique identifier of the tenant.
        status (Status): The acknowledgement status containing status code, and description.
    """

    request_id: str
    turn_id: str
    session_id: str
    tenant_id: str

    status: Status
