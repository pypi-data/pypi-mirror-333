class ParseError(Exception):
    """When parsing the digest file fails."""
    pass

class RestoreError(Exception):
    """General exception for when project restoration fails."""
    pass