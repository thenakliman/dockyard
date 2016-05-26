import ast
import json

def json_dump(data):
    """This function dumps data into json format to send over the internet.
    """
    return json.dumps(data)

def str_to_dict(data):
    """This function convert string to dict.
    """
    return ast.literal_eval(data)
