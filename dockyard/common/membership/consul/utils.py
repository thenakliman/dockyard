# This module contains utility required by consul driver only.

def get_formatted_hosts(services):
    """This method is responsible for formatting output as per
       need of the dockyard.
    """
    healthy_services = []
    for service in services[1]:
        service_info = dict()
        service_info["host"] = str(service["Service"]["Address"])
        service_info["port"] = service["Service"]["Port"]
        healthy_services.append(service_info)

    return healthy_services
