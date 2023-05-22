#!/bin/bash

# run script to retrieve IPv6 addresses and store in local directory
conda activate py3_env && \
python ./ipv6_retrieval/ipv6_retrieval.py

# run script to identify aliased addresses and create alias using predefine algorithm
python ./ipv6_retrieval/ipv6_identify_prefixes.py

# run zmapv6 scan in order to select de-aliased IPv6 addresses and store them
#bash ./2-dealiase_addresses.sh