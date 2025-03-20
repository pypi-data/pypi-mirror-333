from pydantic import BaseModel
from typing import Dict, Any, Optional


class QueryRequest(BaseModel):
    """
    Represents a request model for executing a query.

    Attributes:
        request_id (str): A unique identifier for the request.
        turn_id (str): The unique identifier of the turn.
        session_id (str): The unique identifier of the session.
        tenant_id (str): The unique identifier of the tenant.
        user (dict): A dictionary containing user details (e.g., user ID, role, security context etc..).
        metadata (dict): A dictionary containing any optional metadata required  to fulfil the request.
        curl (str): The cURL command representation of the external request (mutually exclusive with query_str, & nl_prompt).
        query_str (str): The request query defined in a valid query language (mutually exclusive with curl, & nl_prompt).
        nl_prompt: The request prompt in natural language (mutually exclusive with query_str, & curl).
    """

    request_id: str
    turn_id: str
    session_id: str
    tenant_id: str
    user: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    curl: Optional[str] = None
    query_str: Optional[str] = None
    nl_prompt: Optional[str] = None
