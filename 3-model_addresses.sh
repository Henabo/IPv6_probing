#!/bin/bash

# ATTENTION - DO NOT RUN AS SINGLE BASH FILE FOR NOW
# NEED TO IMPLEMENT WORKING SWITCH BETWEEN DEFAULT(PY3), PY2 AND DEFAULT(PY3) ENVS TO NOT BREAK

# transform ipv6 addresses in hex IP format (32 hex characters per line, no colons) for entropy-ip
# conda activate py3_env && \
# python ./ipv6_retrieval/ipv6_transform.py > python ./ipv6_retrieval/ipv6_transform.py > ./ipv6_hitlists/transformed_ipv6_addresses.txttransformed_ipv6_addresses.txt
python3 ./ipv6_retrieval/ipv6_transform.py > ./ipv6_hitlists/transformed_ipv6_addresses.txt
# run script to generate Bayesian Modeling of de-aliased IPv6 addresses for addresses' generation
# conda activate py2_env && \
cd entropy-ip && \
bash ./ALL.sh ../ipv6_hitlists/transformed_ipv6_addresses.txt ../ipv6_model

# go back to working directory
cd ..
#conda deactivate
