

def string_sanitize(value: str) -> str:
    """
    Remove all characters that is not alphanumeric and spaces
    """
    return ''.join(e.lower() for e in value if e.isalnum() or e == ' ')

class YoutubeUnavailable(Exception):
    pass