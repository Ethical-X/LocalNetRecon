import detect_interfaces
import scan
import ipaddress
import re

def print_output(results):
    try:
        lines = results.split("\n")
        for line in lines:
            print(f"| {line}")
    except AttributeError:
        print(results)


def choose_interface():
    detected_interfaces = detect_interfaces.grab_interfaces()
    # Puts all interface names in a list to use for choosing an interface later.
    interfaces_list = [interface for interface in detected_interfaces]
    interface_num = 0
    interface_selected = None

    # Trows an error if no interfaces are detected.
    if len(detected_interfaces) == 0:
        print("| NO USABLE INTERFACES DETECTED!")
        print("| Make sure you are connected to a Network and your interface is up.")
        return

    # If only one interface is detected it defaults to it.
    elif len(detected_interfaces) == 1:
        print("| Detected only 1 usable interface:")
        for i in detected_interfaces:
            print(f"| {interface_num}. Name: {i} | IP: {detected_interfaces[i][0]} | NETMASK: {detected_interfaces[i][1]}")
        interface_selected = i

    # Else if multiple interfaces are detected it asks the user which interface to use.
    else:
        print(f"| Detected {len(detected_interfaces)} Interfaces:")
        for i in detected_interfaces:
            print(f"| {interface_num}. Name: {i} | IP: {detected_interfaces[i][0]} | NETMASK: {detected_interfaces[i][1]}") 
            interface_num += 1

        while True:
            try:
                interface_selected = int(input("| Specify an interface: "))
                if interface_selected < 0 or interface_selected > len(detected_interfaces) - 1:
                    print("| Invalid input!")
                    continue
                interface_selected = interfaces_list[interface_selected]
                break
            except ValueError:
                print("| Invalid Input!")

    # Finds the cidr and network address to pass into nmap.
    cidr = ipaddress.IPv4Network(f"{detected_interfaces[interface_selected][0]}/{detected_interfaces[interface_selected][1]}", strict=False).prefixlen
    network_addr = str(ipaddress.IPv4Network(f"{detected_interfaces[interface_selected][0]}/{cidr}", strict=False))
    user_ip = detected_interfaces[interface_selected][0]

    return network_addr,user_ip


def get_ips(scan_output):
    # Grabs every IPv4 looking address from the nmap scan results.
    iplist = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", scan_output)
    valid_ips = []
    # checks if every result retruned from re.findall is a valid IPv4 address and removes any invalid IP's.
    for ip in iplist:
        try:
            ipaddress.IPv4Address(ip)
            valid_ips.append(ip)
        except ipaddress.AddressValueError:
            continue
    return valid_ips


# This is to ask the user yes or no questions.
def answer():
    while True:
        user_choice = input("|: ")
        if user_choice.lower() == "n" or user_choice.lower() == "no":
            return False
        elif user_choice.lower() == "y" or user_choice.lower() == "yes":
            return True
        print("| Please enter y/yes or n/no")


# This prints all ip's available for scanning and prompts the user to choose which to scan.
def choose_ip(iplist, user_ip):
    ip_num = 0
    available_ips = []
    chosen_ips = []

    for ipaddr in iplist:
        if ipaddr != user_ip:
            available_ips.append(ipaddr)

    for ip in available_ips:
        print(f"| {ip_num}. {ip}")
        ip_num += 1

    try:
        option = input("|: ")

        if option:
            option = option.split(",")
            for num in option:
                # Filters any invalid input like a character,empty input or number outside of the available_ips.
                if num:
                    if not num.isdigit() or int(num) < 0 or int(num) >= ip_num:
                        print(f"| SKIPPING INVALID OPTION: {num}")
                        continue
                    else:
                        chosen_ips.append(available_ips[int(num)])
    except IndexError as e:
        print(f"| ERROR: {e}")

    return chosen_ips, available_ips


def main():
    print("======== Local Network Recon Tool V1. ========" )
    print("| Detecting Usable Interfaces.....")
    
    try:
        network_addr,user_ip = choose_interface()
    except TypeError:
        return

    if not network_addr and not user_ip:
        return

    print("| ============================================")
    print("| PERFORMING HOST DISCOVERY ON LOCAL NETWORK.|")
    print("| ============================================")

    scan_output = str(scan.host_discovery(network_addr))
    print_output(scan_output)
    iplist = get_ips(scan_output)

    print("| ===================================")
    print("| NMAP HOST DISCOVERY SCAN COMPLETED.")
    print("| Proceed with scanning individual IP'S? (Yes/No)")

    y_or_n = answer()

    if not y_or_n:
        print("| Exiting...")
        return

    print("| =====================")
    print("| Choose an IP'S to scan comma seperated e.g (0,1,2) or press enter to scan all:")

    ips_selected, available_ips = choose_ip(iplist, user_ip)

    if ips_selected:
        print(f"| Selected IPS: {ips_selected}")
    else:
        print(f"| Selected ALL IPS")
        ips_selected = available_ips
    
    print("| Would you like to Specify scan flags?")
    select_flags = answer()

    if select_flags:
        print("| Would you like to use the same flags for every scan?")
        flags_option = answer()

    if select_flags and flags_option:
        print("| Enter flags space-seperated e.g (-p 80,443 -sV)")
        flags = input("|: ")
        print("| =============================================")

        for ip in ips_selected:
            scan_output = scan.scan_host(ip,flags)
            print_output(scan_output)
            print("| ============================================")

    elif select_flags:

        for ip in ips_selected:
            print(f"| Enter flags for {ip} space-seperated e.g (-p 80,443 -sV)")
            flags = input("|: ")
            print("| =============================================")
            scan_output = scan.scan_host(ip, flags)
            print_output(scan_output)
            print("| =============================================")

    else:
        flags = []
        print("| Using basic nmap scan: (nmap IP)")
        for ip in ips_selected:
            scan_output = scan.scan_host(ip, flags)
            print_output(scan_output)

    print("| ======= GOODBYE :) =======")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n| Exiting...")

