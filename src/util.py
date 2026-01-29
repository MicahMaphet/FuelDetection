def path_to_obj(s: list) -> dict:
    if len(s) == 1:
        return { s[0]: {} }
    else:
        return { s[0]: path_to_obj(s[1:]) }

def merge(d1: dict, d2: dict):
    result = d1.copy()
    for key in d2.keys():
        if key in d1.keys():
            result[key] = merge(d1[key], d2[key])
        else:
            result[key] = d2[key]
    return result
