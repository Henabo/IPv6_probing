# IPv6_probing
Repository to check existence of IPv6 address and check validity avoiding aliases

# Prerequisites
## python environments - READ CAREFULLY
@DressPD 
* local installation of python 3.8+, 2.7 and Linux terminal (bash, zsh also via WSL) with valid connetivity and SUDO option available
* install package manager (conda, pip or apt) with the following virtual environments: py2_env, py3_env
* as defined in create_py_envs.txt
* docker images and containers could have been considered to deploy and manage dependencies with larger time
## Zmap Scanner set up and configuration - READ CAREFULLY
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

## Entropy-ip set up and configuration - READ CAREFULLY
@DressPD
to set up entropy-ip:
1. run ```git clone https://github.com/akamai/entropy-ip.git``` in terminal in current reporitory to extract the source code
2. run ```./create_py2_env.sh``` to set up a conda enviroment with python 2 and necessary packages for entropy-ip (consider pip or atp as alternative solutions)
to run entropy-ip for addresses generation:
1. Prepare your IPv6 dataset in hex IP format (32 hex characters per line, no colons)
2. Change working directory to newly generated repository and activate py2_env
3. Run ```./ALL.sh <ips> <target>```, where ```<ips>``` is your dataset file, and ```<target>``` is the output directory for storing the results

# Instructions to run the experiment
## 1. IPv6 retrieval and aliasing
@DressPD  
to execute the operation, perform the following processes:
1. open a bash terminal in a folder containing this repository (locally or via ssh)
2. run ```chmod +x retrieve_addresses.sh``` to allow execution of customs bash files
3. execute ```./retrieve_addresses.sh``` that will download weekly list of actives addresses and decode into a local .txt file:
    1. ipv6_retrieval.py will be executed downloading and storing in the working directory ipv6 hitlist called responsive_ipv6_addresses.txt
    2. ipv6_identify_prefixes.py will iterate the hitlist, remove aliased addresses in /64 prefix and generate 1 pseudo-random address for each 4-bit /68 subprefix storing the output in a list and file called aliased_ipv6_addresses.txt

## 2. Scan IPv6 addresses and de-aliasing
@zhang12574  
1. the file aliased_ipv6_addresses.txt contains a list structured of 1 original address and 16 aliases every 17 lines. Zmpav6 will send 16 packets to aliased addresses (pseudo-random addresses within generated addresses in IPv6 prefix) using TCP/80 and ICMPv6 enforcing traversal of a subprefix with different nybbles. SUDO permissions required for Linux kernel
2. responsive addresses are counted. If we obtain responses from all 16 (either TCP/80 or ICMPv6 is ok) , we label the prefix as aliased and remove it. If not, we write the original address (line 1) in a file called dealiased_ipv6_addresses.txt
3. `./dealiase_addresses.sh` will do the previous two jobs, and it is included and called also in `./retrieve_addresses.sh`

## 3. Generate new IPv6 Addresses using entropy-ip
@DressPD
open a bash terminal in a folder containing this repository (locally or via ssh)

2. run ```chmod +x generate_addresses.sh``` to allow execution of customs bash files
3. execute ```./generate_addresses.sh``` that will provide the folllowing tasks: 
   1. ipv6_transform.py will prepare dealiased_ipv6_addresses.txt IPv6 list in hex IP format (32 hex characters per line, no colons)
   2. ```./ALL.sh <ips> <target>``` will generate new ipv6 addresses based on the input file
   3. new addresses will be stored in the folder generated_ipv6_addresses for further analysis

## 4. Scan de-aliased and generated IPv6 addresses for one week - MISSING
@zhang12574  
1. set up daily scanning using Cronjob or equivalent methods
2. save results in a folder measuring responsiveness

## 5. Daily active IPv6 addresses report and results - MISSING
@zhang12574
1. plot results and analysis (using python script or BI tool)
2. produce instructions and interpretation of results

_server new password: `fiagroup4`_
