
def make_url(host='127.0.0.1', port=None, protocol='http', url=None):
    head = protocol + '://'
    head = head + host
    if port: 
        head = head + ":" + port

    if url:
        url = head + url
    else:
        url = head

    return url

def make_query_url(kwargs):
    url = ''
    for key, value in kwargs.iteritems():
        url += key + '=' + value + '&'
    url = url[:-1]
    return url
