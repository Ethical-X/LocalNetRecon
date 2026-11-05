import psutil
import socket
import ipaddress

# Grabs all interfaces
def grab_interfaces():

    interfaces_to_use = dict()
    interfaces_dict = psutil.net_if_addrs()

    for interface in interfaces_dict:
        for address in interfaces_dict[interface]:

            # rejects any non ipv4 addresses and loopback addresses.
            if address.family != socket.AF_INET or address.netmask == None or ipaddress.ip_address(address.address).is_loopback:
                continue

            interfaces_to_use.update({interface: [address.address, address.netmask]})
            break

    return interfaces_to_use

