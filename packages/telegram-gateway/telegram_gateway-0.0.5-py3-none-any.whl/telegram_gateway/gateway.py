import requests

from . import constants, types

class TelegramGateway:
    """The TelegramGateway class is used to interact with the Telegram Gateway."""
    
    """The API token."""
    api_token: str
    
    @property
    def _headers(self) -> str:
        return dict(authorization=f"Bearer {self.api_token}")
    
    def __init__(self, api_token: str) -> None:
        """Create an object of TelegramGateway to access the API.

        Arguments:
            api_token -- Your token.
        """
        self.api_token = api_token
    
    def sendVerificationMessage(self, phone_number: str, code: str | int | None = None, code_length: int | None = None, sender_username: str | None = None, request_id: str | None = None, callback_url: str | None = None, payload: str | None = None, ttl: int | None = None) -> types.RequestStatus:
        """Send a verification message to the specified phone number.

        Arguments:
            phone_number -- The phone number to send the message to. Must be in the E.164 format.

        Keyword Arguments:
            code -- The verification code. Use this parameter if you want to set the verification code yourself. Only fully numeric strings between 4 and 8 characters in length are supported. (default: {None})
            code_length -- The length of the verification code if Telegram needs to generate it for you. Supported values are from 4 to 8. This is only relevant if you are not using the code parameter to set your own code. Use the checkVerificationStatus method with the code parameter to verify the code entered by the user. (default: {None})
            sender_username -- Username of the Telegram channel from which the code will be sent. The specified channel, if any, must be verified and owned by the same account who owns the Gateway API token. (default: {None})
            request_id -- The unique identifier of a previous request from checkSendAbility. If provided, this request will be free of charge, so specify this argument if you used checkSendAbility and don't want your cost to double. (default: {None})
            callback_url -- A URL where you want to receive delivery reports related to the sent message. (default: {None})
            payload -- Custom payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes. (default: {None})
            ttl -- Time-to-live (in seconds, 30...3600) before the message expires and is deleted. The message will not be deleted if it has already been read. If a message is not delivered within the specified ttl, the request fee will be refunded automatically. If a message is successfully delivered within the ttl, it will not be refunded. If not specified, the message will not be deleted. (default: {None})
            
        Raises:
            ValueError: Raised if you specified both code and code_length, and len(code) != code_length.
            ValueError: Raised if the code is not 4 to 8 digits long.
            ValueError: Raised if ttl is less than 30 or bigger than 3600.
            ValueError: Raised if the amount of bytes in payload (encoded with utf-8) is bigger than 128.
            ValueError: Raised if the code is not a number.
            RuntimeError: Telegram Gateway returned an error.
        
        Returns:
            A RequestStatus object.
        """
        if code:
            code = str(code)
        
        if code and code_length and len(code) != code_length:
            raise ValueError("Both code and code_length options are set, and the length of the code isn't equal to the code_length option.")

        if (code_length and not code_length in range(4, 9)) or (code and len(code) not in range(4, 9)):
            raise ValueError("The code is not 4 to 8 digits long.")

        if code and not code.isdigit():
            raise ValueError("The code is not a number.")
        
        if ttl and (ttl < 30 or ttl > 3600):
            raise ValueError("TTL is less than 30 or bigger than 3600.")
        
        if payload and len(payload.encode()) > 128:
            raise ValueError("The amount of bytes in payload (encoded with utf-8) is bigger than 128 bytes.")
        
        result = requests.post(constants.SEND_VERIFICATION_MESSAGE_URL, headers=self._headers, data={
            'phone_number': phone_number,
            'request_id': request_id,
            'sender_username': sender_username,
            'code': code,
            'code_length': code_length,
            'callback_url': callback_url,
            'payload': payload,
            'ttl': ttl
        }).json()
        
        if not result.get('ok'):
            raise RuntimeError(result.get('error', 'Unknown error.'))
        
        return types.RequestStatus.load_from_dict(result['result'])
    
    def checkSendAbility(self, phone_number: str) -> types.RequestStatus:
        """Use this method to check the ability to send a verification message to the specified phone number. If the ability to send is confirmed, a fee will apply according to the pricing plan. If not, the request is free of charge, and an exception gets raised. After checking, you can send a verification message using the sendVerificationMessage method. Make sure to provide the request_id from the response to avoid being billed twice for your request.

        Arguments:
            phone_number -- The phone number in E.164 format

        Raises:
            RuntimeError: If Telegram returns an error.
        
        Returns:
            A RequestStatus object, as if you were to actually sent a verification message.
        """
        
        result = requests.post(constants.CHECK_SEND_ABILITY_URL, headers=self._headers, data={
            'phone_number': phone_number
        }).json()
        
        if not result.get('ok'):
            raise RuntimeError(result.get('error', 'Unknown error.'))
        
        return types.RequestStatus.load_from_dict(result['result'])
    
    def checkVerificationStatus(self, request_id: str, code: str | int | None = None) -> types.RequestStatus:
        """Use this method to check the status of a verification message that was sent previously. If the code was generated by Telegram for you, you can also verify the correctness of the code entered by the user using this method. You can call this method even if you passed in your own code, it will still work as expected and will allow you to track the conversion rate in the Telegram gateway admin panel.

        Arguments:
            request_id -- The unique identifier of the verification request whose status you want to check.

        Keyword Arguments:
            code -- The code entered by the user. If provided, the method checks if the code is valid for the relevant request. (default: {None})

        Raises:
            ValueError: If the code is not 4 to 8 digits long.
            ValueError: If the code is not a number.
            RuntimeError: Telegram Gateway returned an error.

        Returns:
            A RequestStatus object. Check RequestStatus.verification_status.status to see if the code the user typed in is correct or not.
        """
        code = str(code)
        
        if code and len(code) not in range(4, 9):
            raise ValueError("The code is not 4 to 8 digits long.")

        if code and not code.isdigit():
            raise ValueError("The code is not a number.")
        
        result = requests.post(constants.CHECK_VERIFICATION_STATUS_URL, headers=self._headers, data={
            'request_id': request_id,
            'code': code
        }).json()
        
        if not result.get('ok'):
            raise RuntimeError(result.get('error', 'Unknown error.'))
        
        return types.RequestStatus.load_from_dict(result['result'])
    
    def revokeVerificationMessage(self, request_id: str) -> None:
        """Use this method to revoke a verification message that was sent previously. This does not guarantee that the message will be deleted. For example, it will not be removed if the recipient has already read it.

        Arguments:
            request_id -- The unique identifier of the request whose verification message you want to revoke.

        Raises:
            RuntimeError: If Telegram Gateway returns an error
            RuntimeError: If Telegram Gateway returns False as the result, meaning that it didn't receive the revocation request.
        """
        
        result = requests.post(constants.REVOKE_VERIFICATION_STATUS_URL, headers=self._headers, data={
            'request_id': request_id
        }).json()
        
        if not result.get('ok'):
            raise RuntimeError(result.get('error', 'Unknown error.'))
        
        if not result.get('result'):
            raise RuntimeError("The revocation request was not received by the server.")