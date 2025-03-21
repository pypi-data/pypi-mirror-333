def extract_tb(tb, limit=None):
    """Extract and return a list of traceback entries."""
    from traceback import extract_tb as original_extract_tb
    return original_extract_tb(tb, limit)


def extract_stack(f=None, limit=None):
    """Extract and return the current stack as a list of traceback entries."""
    from traceback import extract_stack as original_extract_stack
    return original_extract_stack(f, limit)
