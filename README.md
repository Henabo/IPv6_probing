# IPv6_probing
Repository to check existence and map IPv6 addressed and check respondse tates while avoiding aliases

存储库检查存在和映射IPv6地址，并检查响应状态，同时避免别名

# Prerequisites 准备环境
## python environments - READ CAREFULLY，Python环境
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
2. read and execute ```0-create_py_envs.txt``` to set up a conda enviroment with python 2 and necessary packages for entropy-ip (consider pip or atp as alternative solutions)
to run entropy-ip for addresses modeling:
1. Prepare your IPv6 dataset in hex IP format (32 hex characters per line, no colons)
2. Change working directory to newly generated repository and activate py2_env
3. Run ```./ALL.sh <ips> <target>```, where ```<ips>``` is your dataset file, and ```<target>``` is the output directory for storing the results

## eip-generator set up and configuration - READ CAREFULLY
@DressPD  
to install eip-generator:
1. run ```https://github.com/pforemski/eip-generator``` in terminal in current reporitory to extract the source code
2. run ```sudo apt-get install golang-go``` to install GO if not available
3. build the program with ```make \ go build -o eip-generator eip-generator.go lib.go```
to run eip-generator for addresses creation:
1. run ```./eip-convert.py ../ipv6_model/segments ../ipv6_model/analysis ../ipv6_model/cpd > ../ipv6_model/eip.model``` to translate the model
2. Change working directory to newly generated repository and activate py2_env
3. Run ```./eip-generator -M 100000 -N 8000000 < ../ipv6_model/eip.model > generated_ipv6_addresses.txt``` to generato 100k new addresses
4. Run ```python3 ipv6_de_transform.py > ../ipv6_hitlists/generated_ipv6_addresses.txt``` to format the addresses
```
  -M int -> max. number of addresses per model state (default 1000)
  -N int -> approx. number of addresses to generate (default 1000000)
  -P int -> max. depth in model to run in parallel (default 4)
  -S float -> minimum state probability, 0 = auto
  -V -> verbose
  -p -> pass stdin to stdout
```

# Instructions to run the experiment
# 运行试验的说明
## 1. IPv6 retrieval and aliasing
## IPv6检索和别名
@DressPD  
to execute the operation, perform the following processes:
1. open a bash terminal in a folder containing this repository (locally or via ssh)
2. run ```chmod +x 1-retrieve_addresses.sh``` to allow execution of customs bash files
3. execute ```./1-retrieve_addresses.sh``` that will download weekly list of actives addresses and decode into a local .txt file:
    1. `ipv6_retrieval.py` will be executed downloading and storing in the working directory ipv6 hitlist called responsive_ipv6_addresses.txt
    2. `ipv6_identify_prefixes.py` will iterate the hitlist, remove aliased addresses in /64 prefix and generate 1 pseudo-random address for each 4-bit /68 subprefix storing the output in a list and file called aliased_ipv6_addresses.txt

## 2. Scan IPv6 addresses and de-aliasing
## IPv6地址去别名
@zhang12574  
1. the file aliased_ipv6_addresses.txt contains a list structured of 1 original address and 16 aliases every 17 lines. Zmpav6 will send 16 packets to aliased addresses (pseudo-random addresses within generated addresses in IPv6 prefix) using TCP/80 and ICMPv6 enforcing traversal of a subprefix with different nybbles. SUDO permissions required for Linux kernel
文件aliased_ipv6_address .txt包含一个由1个原始地址和16个别名组成的列表，每17行。Zmpav6将发送16个数据包到别名地址(在IPv6前缀中生成地址中的伪随机地址)，使用TCP/80和ICMPv6强制遍历具有不同nybbles的子前缀。Linux内核所需的SUDO权限
2. responsive addresses are counted. If we obtain responses from all 16 (either TCP/80 or ICMPv6 is ok) , we label the prefix as aliased and remove it. If not, we write the original address (line 1) in a file called dealiased_ipv6_addresses.txt
响应地址被计数。如果我们从所有16个(TCP/80或ICMPv6都可以)获得响应，我们将前缀标记为别名并删除它。如果不是，我们将原始地址(第1行)写入名为dealiased_ipv6_addresses.txt的文件中
3. ```chmod +x dealiase_addresses.sh``` to allow execution of customs bash files
4. `./2-dealiase_addresses.sh` will do the previous two jobs, and it is included and called also in `./1-retrieve_addresses.sh`


## 3. Model IPv6 Addresses using entropy-ip
@DressPD  
1. open a bash terminal in a folder containing this repository (locally or via ssh)
2. run ```chmod +x 3-model_addresses.sh``` to allow execution of customs bash files
3. execute ```./3-model_addresses.sh``` that will provide the folllowing tasks: 
   1. `ipv6_transform.py` will prepare dealiased_ipv6_addresses.txt IPv6 list in hex IP format (32 hex characters per line, no colons)
   2. ```./ALL.sh <ips> <target>``` will generate new ipv6 model based on the input hitlist
   3. new addresses will be stored in the folder ipv6_model for further analysis

## 4. Generate new IPv6 Addresses using eip-generator
@DressPD  
1. run ```chmod +x 4-generate_addresses.sh``` to allow execution of customs bash files
2. execute ```./4-generate_addresses.sh``` that will provide the folllowing tasks: 
   1. `eip-convert.py` will convert the previous model in readble input to generat addresses
   2. ```./eip-generator``` will generate new ipv6 addresses based on the input file
   3. new addresses will be stored in generated_ipv6_addresses.txt

## 5. Scan de-aliased and generated IPv6 addresses for one week
@zhang12574  
1. run ```chmod +x 5-scan_all.sh``` to allow execution of customs bash files
2. run `./5-scan_all.sh` daily to get the scan result for de-aliased and generated addresses and produce reports in dedicate folder
3. it was not possible for us to set up daily scanning using Cronjob or equivalent methods, but it would have been a cool strategy to partially automate the process

## 6. Daily active IPv6 addresses report and results
@zhang12574
1. Once the 7 daily reports are available and stored in the target folder
1. run ```chmod +x 6-analysis.sh``` to allow execution of customs bash files
2. run `./6-analysis.sh`  
   1. `result_aggregate.py` will aggregate the results in numerical format from the responses collected
   2. `plotting.py` will iterate the named files and produce a line chart showing the hit ratio per day in the reports folder
   3. Remember to check the files to adjust hard-coded paramaters as hitlists size and files name
