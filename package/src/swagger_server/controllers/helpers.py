from bson import ObjectId

def check_id(f):

    def wrapper(*args, **kwargs):
        try:
            ObjectId(kwargs.get('id'))
            return f(*args, **kwargs)
        except:
            return {"ERROR": "Invalid id"}, 400

    return wrapper

def _stringify_object_id(result):
    stringified_result = []
    for element in result:
        element['_id'] = str(element['_id'])
        stringified_result.append(element)
    return stringified_result

def _calculate_quote(query_id):
    return 4000