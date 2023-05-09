import os
import requests
import lzma

#define import url and filename
url = 'https://alcatraz.net.in.tum.de/ipv6-hitlist-service/open/responsive-addresses.txt.xz'
filename = './ipv6_hitlists/responsive_ipv6_addresses.txt.xz'

#use request library to download file
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

#decode .xz in .txt for readability
with lzma.open(filename) as f:
    uncompressed_content = f.read().decode('utf-8')

#save it in current working directory
with open('./ipv6_hitlists/responsive_ipv6_addresses.txt', 'w') as f:
    f.write(uncompressed_content)