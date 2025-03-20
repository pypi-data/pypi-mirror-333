# vrint.py
import inspect

verbose = True  # Default global setting

def vrint(*args, verbose=None, **kwargs):
    """
    Prints the given arguments only if verbose is True.
    
    Parameters:
    *args: Arguments to be printed
    verbose: Optional boolean to override the caller's verbose setting
    **kwargs: Keyword arguments passed to print function
    """
    # If verbose parameter is provided, use it
    if verbose is not None:
        use_verbose = verbose
    else:
        # Otherwise try to get the verbose from caller's frame
        caller_frame = inspect.currentframe().f_back
        caller_globals = caller_frame.f_globals
        caller_locals = caller_frame.f_locals
        
        # First check if verbose exists in caller's local variables
        if 'verbose' in caller_locals:
            use_verbose = caller_locals['verbose']
        # Then check if verbose exists in caller's global variables
        elif 'verbose' in caller_globals:
            use_verbose = caller_globals['verbose']
        # Fallback to our module's default verbose setting
        else:
            use_verbose = globals()['verbose']
        
    if use_verbose:
        print(*args, **kwargs)
