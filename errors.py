class FileException(Exception):
    """Fatal File Exception"""

    pass


class BoardException(Exception):
    """Fatal Board Exception"""

    pass


class CellException(Exception):
    """Fatal Cell Exception"""

    pass


class DeserializerException(Exception):
    """Non-Fatal Deserializer Exception"""

    pass
