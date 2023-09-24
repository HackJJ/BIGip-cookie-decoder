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

def encode_to_cookie(ip_port):
    try:
        ip, port_str = ip_port.split(':')
        a, b, c, d = [int(i) for i in ip.split('.')]
        port = int(port_str)
        if port < 0 or port > 65535:
            raise ValueError
    except ValueError:
        print("Error: Invalid IP:Port format. Expected format is 'x.x.x.x:yyyy' where yyyy is between 0 and 65535.")
        return

    host = struct.unpack("<I", bytes([a, b, c, d]))[0]
    port = struct.unpack("<H", bytes([port // 256, port % 256]))[0]

    # Prompt for the pool name
    pool_name = input("Enter the pool name: ")

    # Construct the cookie value
    cookie_value = f"{host}.{port}.0000"
    print(f"[*] Encoded Cookie: BIGipServer{pool_name}={cookie_value}\n")

# Check if the correct number of arguments are provided
if len(sys.argv) not in [2, 3]:
    print(f"Usage: {sys.argv[0]} cookie OR {sys.argv[0]} x.x.x.x yyyy")
    exit(1)

if len(sys.argv) == 2:
    # Extract the cookie value from the command line argument
    cookie = sys.argv[1]
    print(f"\n[*] Cookie to decode: {cookie}\n")
    # Decode the cookie
    decode_cookie(cookie)
elif len(sys.argv) == 3:
    # Extract the IP and port from the command line arguments
    ip_port = f"{sys.argv[1]}:{sys.argv[2]}"
    print(f"\n[*] IP:Port to encode: {ip_port}\n")
    # Encode the IP and port to cookie
    encode_to_cookie(ip_port)
