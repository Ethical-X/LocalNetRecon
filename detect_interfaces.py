import psutil

# Grabs all interfaces
def grab_interfaces():

    interfaces_to_use = dict()
    interfaces_dict = psutil.net_if_addrs()

    for interface in interfaces_dict:
        # Avoids adding loopback addresses and unusable interfaces.
        if interface != "lo" and interfaces_dict[interface][0].netmask != None and interfaces_dict[interface][0].netmask != "ffff:ffff:ffff:ffff::":
            # Adds every interface to interfaces_to_use with its ip and netmask to display later on.
            interfaces_to_use.update({interface: [interfaces_dict[interface][0].address, interfaces_dict[interface][0].netmask]})
    
    return interfaces_to_use

