import consul

class ConsulKV(object):
    def __init__(self):
        self.consul = consul.Consul()

    def get(self, key):
        self.consul.kv.get(key)

    def get(self, key, value):
        self.consul.kv.put(key, value)
