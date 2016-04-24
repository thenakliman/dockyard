def make_url(host='127.0.0.1', port=None, protocol='http', url=None):
    head = (("%s://%s") % (protocol, host))
    if port:
        head = (("%s:%s") % (head, port))

    if url:
        url = (('%s%s') % (head, url))
    else:
        url = head

    return url


def make_query_url(kwargs):
    url = ''
    for key, value in kwargs.iteritems():
        url += (('%s=%s&') % (key, value))
    url = url[:-1]
    return url
