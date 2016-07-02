import consul

class ConsulKV(object):
    def __init__(self):
        self.consul = consul.Consul()

    def get(self, key):
        return self.consul.kv.get(key)

    def put(self, key, value):
        return self.consul.kv.put(key, value)
