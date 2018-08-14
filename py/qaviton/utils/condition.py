def any_in_any(a, b):
    if len([x for x in a if x in b]) > 0:
        return True
    else:
        return False


def all_in_any(a, b):
    if len([x for x in a if x in b]) == len(a):
        return True
    else:
        return False


def all_in_all(a, b):
    if len([x for x in a if x in b]) == len(a) == len(b):
        return True
    else:
        return False