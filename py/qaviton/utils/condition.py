def any_in_any(a, b):
    if len([x for x in a if x in b]) > 0:
        return True
    else:
        return False
