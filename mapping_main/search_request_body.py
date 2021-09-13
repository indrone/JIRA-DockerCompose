

def dict_search(search_item, data):
    """
    Search for keys/list of keys in a complex/nested dictionary or json object
    """
    found = {}
    if type(search_item) != type([]):
        search_item = [search_item]

    if type(data) == type(dict()):
        for item in search_item:
            if item in data.keys():
                found[item] = data[item]
            elif len(data.keys()) > 0:
                for key in data.keys():
                    result = dict_search(item, data[key])
                    if result:
                        for k, v in result.items():
                            found[k] = v
    elif type(data) == type([]):
        for node in data:
            result = dict_search(search_item, node)
            if result:
                for k, v in result.items():
                    found[k] = v
    return found
