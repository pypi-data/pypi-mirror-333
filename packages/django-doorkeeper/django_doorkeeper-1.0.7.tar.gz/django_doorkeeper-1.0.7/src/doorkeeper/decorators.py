def doorkeeper_exempt(view_func):
    """
    Decorator that marks a view as exempt from the doorkeeper protection.
    """
    # Mark the view function as exempt
    view_func.doorkeeper_exempt = True
    return view_func
