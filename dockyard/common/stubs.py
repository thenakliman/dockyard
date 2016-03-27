import subprocess

def send_request(url ,data):
    headers = 'Content-Type: application/json'
    command = "curl -H '%s' %s -d '%s'" % (headers, url, data)
    print command
    output = subprocess.check_output(command.split())
    #req = urllib2.Request(url, data, headers)
    return str(output)

#send_request('localhost:3333', {'aaaa'})
