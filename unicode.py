import unicodedata


def strip_accents(text: str) -> str:
    """Remove accents from a string"""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    )


def normalize_json_text(data):
    """
    Recursively walk through dicts/lists/strings
    and strip accents.
    """

    if isinstance(data, dict):
        return {k: normalize_json_text(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_json_text(v) for v in data]
    elif isinstance(data, str):
        return strip_accents(data)
    else:
        return data
