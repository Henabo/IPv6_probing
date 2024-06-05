import os
import ipaddress
import random
from multiprocessing import Pool, Manager, freeze_support

# 别名消除
def aliase_removal(addrs, hits_1, hits_2):
    result = []
    assert(len(addrs) % 17 == 0)
    ind1, ind2 = 0, 0
    prefixmap = {}
    # as zmap result breaks the order of addresses, serial traversal doesn't work
    # Generate dict with prefixes as keys
    # 循环1: 遍历addrs列表，以17个地址为一组，创建网络前缀，并将其添加到prefixmap字典中。
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
    # 循环2: 遍历hits_1列表，检查每个响应地址是否存在于prefixmap中对应的生成地址列表中，如果存在，标记该地址为响应。
    for ind1 in range(len(hits_1)):
        ip = ipaddress.ip_address(hits_1[ind1])
        prefix = ipaddress.ip_network(ip.exploded + '/64', strict=False)
        if hits_1[ind1] in prefixmap[prefix][1]:
            idx1 = prefixmap[prefix][1].index(hits_1[ind1])
            if (prefixmap[prefix][2][idx1] == 0):
                prefixmap[prefix][3] += 1       # total responsive cnt
                prefixmap[prefix][2][idx1] = 1  # responsive mark
    # Traverse hitlist 2 to mark responsive addresses
    # 环3: 类似于循环2，但是针对hits_2列表。
    for ind2 in range(len(hits_2)):
        ip = ipaddress.ip_address(hits_2[ind2])
        prefix = ipaddress.ip_network(ip.exploded + '/64', strict=False)
        if hits_2[ind2] in prefixmap[prefix][1]:
            idx2 = prefixmap[prefix][1].index(hits_2[ind2])
            if (prefixmap[prefix][2][idx2] == 0):
                prefixmap[prefix][3] += 1
                prefixmap[prefix][2][idx2] = 1
    # 检查每个前缀的响应计数，如果响应计数小于16（即不是所有生成地址都有响应），则将原始地址添加到结果列表result中。
    for k in prefixmap.keys():
        # if prefixmap[k][3] < 16: # 改为15，因为有可能存在丢包的情况
        if prefixmap[k][3] < 10: 
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

