import subprocess
import shlex

def host_discovery(iprange):
    try:
        result = subprocess.run(["nmap", "-sn", iprange], capture_output=True, text=True)
        return result.stdout
    except PermissionError as e:
        print(f"Permission Denied: {e}")


def scan_host(ip, flags):

    if flags:
        flags = shlex.split(flags)
        cmd = ["nmap"] + flags + [ip]
    else:
        cmd = ["nmap"] + [ip]

    try:

        cmd_show = " ".join(cmd)
        print(f"| Running: {cmd_show} on: {ip}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("| [!] Nmap returned an error:")
            print(result.stderr)
            return
        return result.stdout

    except PermissionError as e:
        print(f"Permission Denied: {e}")

