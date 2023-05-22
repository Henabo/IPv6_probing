import socket
import struct
import ipaddress

def int2ipv6(ip_int):
    hi = (ip_int >> 64) & 0xFFFFFFFFFFFFFFFF
    lo = (ip_int & 0xFFFFFFFFFFFFFFFF)
    ip_int_str = struct.pack('!QQ', hi, lo)
    return socket.inet_ntop(socket.AF_INET6, ip_int_str)

# read input file
with open('./eip-generator/generated_ipv6_addresses.txt', 'r') as f:
    for i, line in enumerate(f):
        address_value = int(line, 16)
        address = int2ipv6(address_value)
        print(address)
        # address = ipaddress.IPv6Address(line.strip())
        # hex_address = format(int(address), '032x')
        # print(hex_address)