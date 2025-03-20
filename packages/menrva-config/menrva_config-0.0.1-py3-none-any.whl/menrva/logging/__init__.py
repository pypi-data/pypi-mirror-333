from uuid import uuid4

__all__ = ["create_identifier"]

def create_identifier() -> str:
    """
    Create a generic identifier which can be used across different
    logging frameworks
    """
    return str(uuid4())