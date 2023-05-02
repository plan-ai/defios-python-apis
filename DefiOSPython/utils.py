from collections import defaultdict


def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False


def remove_dups_by_id(obj_array):
    new_obj_array = []
    key_exists = defaultdict(int)
    for obj in obj_array:
        if key_exists[obj["_id"]] == 0:
            new_obj_array.append(obj)
            key_exists[obj["_id"]] += 1
    return new_obj_array
