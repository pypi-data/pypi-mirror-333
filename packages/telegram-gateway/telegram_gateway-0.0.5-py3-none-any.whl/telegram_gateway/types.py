from dataclasses import dataclass
from . import enums

@dataclass
class VerificationStatus:
    """Dataclass for the verification_status. It contains the code status (valid/invalid), the time it was updated at and, optionally, the code entered."""
    status: enums.VerificationResult
    updated_at: int
    code_entered: str | None = None

@dataclass
class DeliveryStatus:
    """Dataclass for the delivery_status. It contains the status of the delivery and the time it was last updated at."""
    status: enums.MessageDelivery
    updated_at: int

@dataclass
class RequestStatus:
    """Dataclass for the RequestStatus response. It contains the request ID, the recipient's phone number, the cost of the request, and optionally, the delivery status, the remaining balance, your custom payload and the verification status."""
    request_id: str
    phone_number: str
    request_cost: float
    remaining_balance: float | None = None
    delivery_status: DeliveryStatus | None = None
    verification_status: VerificationStatus | None = None
    payload: str | None = None
    is_refunded: bool | None = None

    @classmethod
    def load_from_dict(cls, data: dict) -> "RequestStatus":
        if data.get('delivery_status'):
            data['delivery_status'] = DeliveryStatus(**data['delivery_status'])
        if data.get('verification_status'):
            data['verification_status'] = VerificationStatus(**data['verification_status'])
        return RequestStatus(**data)