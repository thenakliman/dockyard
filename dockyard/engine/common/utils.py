import ast
import json
import netifaces

def json_dump(data):
    """This function dumps data into json format to send over the internet.
    """
    return json.dumps(data)

def str_to_dict(data):
    """This function convert string to dict.
    """
    return ast.literal_eval(data)

def get_localhost_ip():
    """This method resturns localhost ip.
    """
    ifs = netifaces.interfaces()
    for i in ifs:
        try:
            addr = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
        except KeyError:
            pass

        if addr == '127.0.0.1':
            continue

        yield addr
