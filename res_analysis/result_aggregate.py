import os

res_dir = "scan_results"
output_dir = "active_iplists"

type_list = ["generated", "dealiased"]
protocol_list = ["icmp", "tcp"]
date_range = range(16 ,23)

dealiased_cnt = 3286446
generated_cnt = 474209368

active_lists = []
for i, d in enumerate(date_range):
    active_lists.append(set())
    for p in protocol_list:
        for t in type_list:
            path = t + "_scan_res_" + p + "_05" + str(d) + ".csv"
            f = open(os.path.join(res_dir, path))
            next(f)
            lines = f.readlines()
            for l in lines:
                active_lists[i].add(l)
    fo = open(os.path.join(output_dir, "active_ipv6_addresses_05" + str(d) + ".txt"), 'w')
    print("05"+str(d)+":", len(active_lists[i]))
    for l in active_lists[i]:
        fo.write(l)

common = active_lists[0]
for i in range(0, len(active_lists) - 1):
    cs = active_lists[i] & active_lists[i+1]
    fo = open(os.path.join(output_dir, "common_active_addresses_"+str(i)+"_"+str(i+1)+".txt"), 'w')
    print(len(cs))
    for l in cs:
        fo.write(l)
    common = common & active_lists[i+1]
print(len(common))
fo = open(os.path.join(output_dir, "global_common_active_addresses.txt"), 'w')
for l in common:
    fo.write(l)