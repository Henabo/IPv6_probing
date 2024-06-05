import os
import matplotlib.pyplot as plt

# res_dir = "scan_results"
res_dir = "ipv6_hitlists"

output_dir = "active_iplists"

type_list = ["generated", "dealiased"]
protocol_list = ["icmp", "tcp"]
date_range = range(16 ,23)

dealiased_cnt = 3286446
generated_cnt = 474209368

hitrates_generated = []
hitrates_dealiased = []
for i, d in enumerate(date_range):
    for t in type_list:
        active_list = set()
        for p in protocol_list:
            # path = t + "_scan_res_" + p + "_05" + str(d) + ".csv"
            path = t + "_scan_res_" + p + ".csv"
            f = open(os.path.join(res_dir, path))
            next(f)
            lines = f.readlines()
            for l in lines:
                active_list.add(l)
        if t == "generated":
            print(str(d) + t + "_hitrate:", len(active_list) / generated_cnt)
            hitrates_generated.append(100*len(active_list) / generated_cnt)
        else:
            print(str(d) + t + "_hitrate:", len(active_list) / dealiased_cnt)
            hitrates_dealiased.append(100*len(active_list) / dealiased_cnt)
# hitrates_dealiased = [0.8, 0,8, 0.9]
plt.plot(range(len(hitrates_generated)), hitrates_generated)
plt.xlabel("time(day)")
plt.ylabel("hitrate(%)")
plt.title("generated addresses hitrate")
plt.savefig(os.path.join("reports", "hitrates_generated.png"))
plt.close()
plt.plot(range(len(hitrates_dealiased)), hitrates_dealiased)
plt.ylabel("hitrate(%)")
plt.title("de-aliased addresses hitrate")
plt.savefig(os.path.join("reports", "hitrates_dealiased.png"))
plt.close()

