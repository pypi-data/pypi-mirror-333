class MessageDelivery(object):
    """Represents the message delivery status. You can see if the recipient even opened the chat with the code or not."""
    SENT = "sent"
    UNREAD = SENT
    READ = "read"
    REVOKED = "revoked"
    CANCELLED = REVOKED

class VerificationResult(object):
    """Represents the code verification result from checkVerificationStatus."""
    CODE_VALID = "code_valid"
    CORRECT_CODE = CODE_VALID
    CODE_INVALID = "code_invalid"
    WRONG_CODE = CODE_INVALID
    CODE_MAX_ATTEMPTS_EXCEEDED = "code_max_attempts_exceeded"
    TOO_MANY_ATTEMPTS = CODE_MAX_ATTEMPTS_EXCEEDED
    EXPIRED = "expired"
    EXPIRED_CODE = EXPIRED