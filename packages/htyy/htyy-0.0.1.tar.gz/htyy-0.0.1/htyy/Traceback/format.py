def format_exception(exc_type, exc_value, exc_traceback, limit=None, chain=True):
    """Format and return a string representation of the exception."""
    from .print import print_tb
    import traceback
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback, limit=limit, chain=chain))
    return tb_str


def format_tb(tb, limit=None):
    """Format a traceback and return it as a list of strings."""
    from traceback import format_tb as traceback_format_tb
    return traceback_format_tb(tb, limit)
