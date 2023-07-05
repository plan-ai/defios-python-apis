from collections import defaultdict


def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False


def remove_dups_by_id(obj_array,check_is_native_token=False):
    new_obj_array = []
    key_exists = defaultdict(int)
    for obj in obj_array:
        if key_exists[obj["_id"]] == 0:
            if check_is_native_token and not obj["project_token"]["token_new"]:
                continue
            new_obj_array.append(obj)
            key_exists[obj["_id"]] += 1
    return new_obj_array
