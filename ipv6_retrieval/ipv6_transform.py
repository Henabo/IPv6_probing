import ipaddress

# read input file
with open('./ipv6_hitlists/responsive_ipv6_addresses.txt', 'r') as f:
    # Skip first line
    next(f)
    #for line in f:
    limit = 10000  # set a limit of 3 lines to be read
    for i, line in enumerate(f):
        if i >= limit:
            break
        address = ipaddress.IPv6Address(line.strip())
        hex_address = format(int(address), '032x')
        print(hex_address)