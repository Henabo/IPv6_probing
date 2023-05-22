import os
import ipaddress
import random
from multiprocessing import Pool, Manager, freeze_support

def aliase_removal(addrs, hits_1, hits_2):
    result = []
    assert(len(addrs) % 17 == 0)
    ind1, ind2 = 0, 0
    prefixmap = {}
    # as zmap result breaks the order of addresses, serial traversal doesn't work
    # Generate dict with prefixes as keys
    for ind0 in range(0, len(addrs), 17):
        ori_addr = addrs[ind0]
        gen_addrs = [addrs[ind0+i] for i in range(1, 17)]
        ip = ipaddress.ip_address(ori_addr)
        prefix = ipaddress.ip_network(ip.exploded + '/64', strict=False)
        # assert(prefix not in prefixmap.keys())
        if (prefix in prefixmap.keys()):
            continue
        found = [0 for i in range(16)]
        foundcnt = 0
        prefixmap[prefix] = [ori_addr, gen_addrs, found, foundcnt]
    # Traverse hitlist 1 to mark responsive addresses
    for ind1 in range(len(hits_1)):
        ip = ipaddress.ip_address(hits_1[ind1])
        prefix = ipaddress.ip_network(ip.exploded + '/64', strict=False)
        if hits_1[ind1] in prefixmap[prefix][1]:
            idx1 = prefixmap[prefix][1].index(hits_1[ind1])
            if (prefixmap[prefix][2][idx1] == 0):
                prefixmap[prefix][3] += 1       # total responsive cnt
                prefixmap[prefix][2][idx1] = 1  # responsive mark
    # Traverse hitlist 2 to mark responsive addresses
    for ind2 in range(len(hits_2)):
        ip = ipaddress.ip_address(hits_2[ind2])
        prefix = ipaddress.ip_network(ip.exploded + '/64', strict=False)
        if hits_2[ind2] in prefixmap[prefix][1]:
            idx2 = prefixmap[prefix][1].index(hits_2[ind2])
            if (prefixmap[prefix][2][idx2] == 0):
                prefixmap[prefix][3] += 1
                prefixmap[prefix][2][idx2] = 1
    for k in prefixmap.keys():
        if prefixmap[k][3] < 16:
            result.append(prefixmap[k][0])
    return result

if __name__ == '__main__':
    # Open the input file and read the lines
    with open('./ipv6_hitlists/aliased_ipv6_addresses.txt', 'r') as f_a, open('./ipv6_hitlists/aliased_scan_res_icmp.csv', 'r') as f_icmp, open('./ipv6_hitlists/aliased_scan_res_tcp.csv', 'r') as f_tcp, open('./ipv6_hitlists/dealiased_ipv6_addresses.txt', 'w') as o:
        # Skip first line
        next(f_icmp)
        next(f_tcp)
        lines_a = f_a.readlines()
        lines_icmp = f_icmp.readlines()
        lines_tcp = f_tcp.readlines()

        # read aliased address list and hit lists
        addresses = [addr.strip() for addr in lines_a]
        hits_icmp = [addr.strip() for addr in lines_icmp]
        hits_tcp = [addr.strip() for addr in lines_tcp]

        dealiased_addresses = aliase_removal(addresses, hits_icmp, hits_tcp)

        # Output de-aliased IPv6 addresses to external file
        for addr in  dealiased_addresses:
            o.write(addr + '\n')

