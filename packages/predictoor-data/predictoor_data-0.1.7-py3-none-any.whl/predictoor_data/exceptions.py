class PredictoorError(Exception):
    """Base exception for predictoor-data package"""
    pass

class InvalidPairError(PredictoorError):
    """Raised when an invalid trading pair/timeframe is provided"""
    pass

class APIError(PredictoorError):
    """Raised when there's an error with the API request"""
    pass
