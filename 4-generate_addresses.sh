#!/bin/bash

# run script to generate new IPv6 addresses based on previous modeling and store them in a file
python ./eip-generator/eip-convert.py ./ipv6_model/segments ./ipv6_model/analysis ./ipv6_model/cpd > ./ipv6_model/eip.model
./eip-generator/eip-generator -M 20000000 -N 1000000000 < ./ipv6_model/eip.model > ./eip-generator/generated_ipv6_addresses.txt
python3 ./ipv6_retrieval/ipv6_de_transform.py > ./ipv6_hitlists/generated_ipv6_addresses.txt

# scan them for one week and generate report of results
# WIP

# -N 80M -> generate active 0.5 M, 1.56%