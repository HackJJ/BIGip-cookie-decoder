import struct
import sys
import re

def decode_cookie(cookie):
    try:
        # Split the cookie into name and value
        cookie_name, cookie_value = cookie.split('=')
    except ValueError:
        print("Error: Invalid cookie format. Expected format is 'name=value'")
        return

    # Search for the pool name in the cookie name
    pool = re.search(r'^BIGipServer([.\w\.]*)', cookie_name)
    if pool is None:
        print("Error: Invalid cookie name. Expected name to start with 'BIGipServer'")
        return

    try:
        # Split the cookie value into host, port, and end values
        host, port, end = cookie_value.split('.')
    except ValueError:
        print("Error: Invalid cookie value format. Expected format is 'host.port.end'")
        return

    try:
        # Decode the host value
        a, b, c, d = [i for i in struct.pack("<I", int(host))]
    except struct.error:
        print("Error: Failed to decode the host value.")
        return

    try:
        # Decode the port value
        e = [i for i in struct.pack("<H", int(port))]
    except struct.error:
        print("Error: Failed to decode the port value.")
        return

    port = f"0x{e[0]:02X}{e[1]:02X}"

    # Print the decoded information
    print(f"[*] Pool name: {pool.group(1)}")
    print(f"[*] Decoded IP and Port: {a}.{b}.{c}.{d}:{int(port, 16)}\n")

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} cookie")
    exit(1)

# Extract the cookie value from the command line argument
cookie = sys.argv[1]
print(f"\n[*] Cookie to decode: {cookie}\n")

# Decode the cookie
decode_cookie(cookie)
