from namespace import DockyardNamespace
psid=[2057]
ns = DockyardNamespace()
for pid in psid:
    ns.cleanup(pid)

