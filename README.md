# IPv6_probing
Repository to check existence of IPv6 address and check validity avoiding aliases

# Prerequisites
## python environment
@DressPD 
* local installation of python 3.8+ and Linux terminal (bash, zsh also via WSL) with valid connetivity and SUDO option available
* install via packet manager (pip or conda) the following python packages:
    * for hitlist retrieval: os, requests, lzma
    * for de-aliasing: scapy, random, multiprocessing
* ...
## Zmap Scanner set up and configuration
@zhang12574  
to install ZMapv6, do:
1. make sure to install all the dependencies of ZMap  
   On Debian-based systems (including Ubuntu), run:  
   ```sudo apt-get install build-essential cmake libgmp3-dev gengetopt libpcap-dev flex byacc libjson-c-dev pkg-config libunistring-dev```
   For other systems, refer to <https://github.com/zmap/zmap/blob/main/INSTALL.md> to install dependencies.  
2. fetch source code  
   Remember to fetch from the **git repo** <https://github.com/tumi8/zmap.git>, and go to **master branch**:  
   ```
   git clone https://github.com/tumi8/zmap.git
   git checkout master
   ```
   **DO NOT** use any version provided by Ubuntu or any release version, none of them support IPv6.  
3. make and install  
   ```
   cmake .
   make -j4
   sudo make install
   ```
   to check whether installed successfully, run:  
   ```
   zmap --version
   zmap --help | grep IPv6
   ```
to scan a list of IPv6 addresses with zmap:  
1. go to sub-dir: ```zmap_scan```
2. get local IPv6 info :IPv6 address and gateway MAC.
3. fill IPv6 address and gateway MAC in zmap_scan_once.sh:  
   ```--ipv6-source-ip=<Your IP> -G <Your MAC> --ipv6-target-file=<Your File>```
   note: gateway MAC maybe not needed.  
4. run the bash script
   ```bash zmap_scan_once.sh```
6. configure Cronjob for one week  
note: **DO NOT** run with proxy or vpn on, make sure to kill them ahead.

# Instructions
## IPv6 retrieval and aliasing
@DressPD  
to execute the operation, perform the following processes:
1. open a bash terminal in a folder containing this repository (locally or via ssh)
2. run ```chmod +x retrieve_addresses.sh``` to allow execution of customs bash files
3. execute ```./retrieve_addresses.sh``` that will download weekly list of actives addresses and decode into a local .txt file
    1. ipv6_retrieval.py will be executed downloading and storing in the working directory ipv6 hitlist called responsive_ipv6_addresses.txt
    2. ipv6_identify_prefixes.py will iterate the hitlist, remove aliased addresses in /64 prefix and generate 1 pseudo-random address for each 4-bit /68 subprefix storing the output in a list and file called aliased_ipv6_addresses.txt

## Scan IPv6 addresses and de-aliasing
@zhang12574  
1. the file aliased_ipv6_addresses.txt contains a list structured of 1 original address and 16 aliases every 17 lines. Zmpav6 will send 16 packets to aliases addresses (pseudo-random addresses within generated addresses in IPv6 prefix) using TCP/80 and ICMPv6 enforcing traversal of a subprefix with different nybbles. SUDO permissions required for Linux kernel
2. responsive addresses are counted. If we obtain responses from all 16, we label the prefix as aliased and remove it. If not, we write the original address (line 1) in a file called dealiased_ipv6_addresses.txt
3. further instructions...

## Generate new IPv6 Addresses
@Takaya  
1. use dealiased_ipv6_addresses.txt as input to generate random addresses with Entropy/IP, 6Gen, or 6Tree
2. store (or add) original and generated addresses in a different file called generated_ipv6_addresses.txt

## Scan de-aliased and generated IPv6 addresses for one week
@zhang12574  
1. set up daily scanning using Cronjob or equivalent methods
2. save results in a folder measuring responsiveness

## Daily active IPv6 addresses report and results
@Takaya 
1. plot results and analysis (using python script or BI tool)
2. produce instructions and interpretation of results

_server new password: `fiagroup4`_
