import os
import ipaddress
import random
from multiprocessing import Pool, Manager, freeze_support

# Function to filter IPv6 addresses by prefix by removing aliases
def filter_prefixes(addresses):
    prefixes = []
    result = []
    total_len = len(addresses)
    for i, address in enumerate(addresses):
        if (i % 1000) == 0:
            print("process: ", str(i * 100 / total_len)+"%")
        ip = ipaddress.ip_address(address)
        prefix = ipaddress.ip_network(ip.exploded + '/64', strict=False)
        if prefix not in prefixes:
            prefixes.append(prefix)
            result.append(str(ip))
    return result


# Parallelize execution to filter IPv6 addresses by prefix by removing aliases
def parallel_filter_prefixes(addresses):
    # Use Manager to created shared list of prefixes between workers
    with Manager() as manager:
        # prefixes = manager.list()
        with Pool() as pool:
            chunk_size = len(addresses) // os.cpu_count()
            # results = pool.map(filter_prefixes, [(addresses[i:i+chunk_size], prefixes) for i in range(0, len(addresses), chunk_size)])
            # note @Zhang: the line above has some bugs in data splitting
            # so I just removed the sharing-list, and the result doesn't have much repeat elements (zero as I checked)
            results = pool.map(filter_prefixes, [addresses[i:i+chunk_size] for i in range(0, len(addresses), chunk_size)])
            return [item for sublist in results for item in sublist]


# Generate 1 pseudo-random address for each 4-bit subprefix
def generate_aliases_chunk(address):
    aliases = []
    ip = ipaddress.ip_address(address)
    network = ipaddress.ip_network(str(ip) + '/64', strict=False)
    # Keep opriginal address
    aliases.append(address)
    for subnet in network.subnets(prefixlen_diff=4):
        random_ip = str(subnet.network_address + random.randint(0, subnet.num_addresses - 1))
        # Append 16 random addresses from /68 sub-prefix
        aliases.append(random_ip)
    return aliases


def generate_aliases_parallel(addresses):
    with Pool() as pool:
        chunk_size = len(addresses) // os.cpu_count()
        results = pool.map(generate_aliases_chunk, addresses, chunksize=chunk_size)
        return [item for sublist in results for item in sublist]

if __name__ == '__main__':
    #freeze_support()
    # Open the input file and read the lines
    with open('./ipv6_hitlists/responsive_ipv6_addresses.txt', 'r') as f, open('./ipv6_hitlists/aliased_ipv6_addresses.txt', 'w') as o:
        # Skip first line
        next(f)
        # lines = f.readlines()[:20000] # to be removed when server is given
        lines = f.readlines()

        # Read the IPv6 addresses from the input file
        addresses = [addr.strip() for addr in lines]

        # Create a set of IPv6 addresses that belong to a prefix
        prefix_addresses = parallel_filter_prefixes(addresses)

        # Create a set of IPv6 addresses that belong to a prefix
        aliased_addresses = generate_aliases_parallel(prefix_addresses)

        # Output filtered IPv6 addresses to external file
        for addr in  aliased_addresses:
            o.write(addr + '\n')

