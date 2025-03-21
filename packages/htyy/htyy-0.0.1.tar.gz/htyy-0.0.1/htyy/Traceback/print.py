import sys

def print_exc(limit=None, file=None):
    """Print the most recent exception with traceback."""
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_type is not None:
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=limit, file=file)


def print_tb(tb, limit=None, file=None):
    """Print a traceback from a traceback object."""
    import traceback
    traceback.print_tb(tb, limit=limit, file=file)
