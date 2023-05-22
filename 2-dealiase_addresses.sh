# scan aliased addresses with zmap, both TCP/80 and ICMPv6
# the scanning result is in aliased_scan_res_tcp.csv and aliased_scan_res_icmp.csv
bash ./aliase_removal/aliased_address_scanning.sh

# use python script to process the results and recognize the aliased prefixes
python aliase_removal/aliase_removal.py
