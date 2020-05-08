# coding=utf-8
"""
filename:snmp_test.py

说明：
使用系统的 snmpwalk 来查询设备信息，需要先安装 snmp
代码 Windows 和 Linux 通用

Windows cmd 调用示例：snmpwalk -v 2c -c public 127.0.0.1 1.3.6.1.2.1.1.1

Windows cmd 下查看某主机（192.168.132.130）信息示例：
snmpwalk -v 2c -c public 192.168.132.130 1.3.6.1.2.1.1.1
"""

import re
import os
import time
import platform
import eel
import json 

if 'Windows' == platform.system():
    hosts = ['192.168.138.128']
else:
    # 在虚拟机运行时则查看本地
    hosts = ['127.0.0.1']
    #hosts = ['192.168.5.2']

def snmpWalk(host, oid):
    result = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:-1]
    return result

# ------------------------------------------------------------
# 获取负载信息
# ------------------------------------------------------------


def getSystem(host):
    system = ':'.join(snmpWalk(host, 'system')[0].split(':')[3:]).strip()
    return system

# ------------------------------------------------------------
#CPU Utilization
@eel.expose
def getCPU(host):
    cpuload=snmpWalk(host, 'UCD-SNMP-MIB::ssCpuUser.0')
    # cpuload=snmpWalk(host, '1.3.6.1.2.1.25.3.3.1.2')
    # num_process = len(cpuload)
    # cpu = 0
    # for i in range(num_process):
    #     temp = snmpWalk(host, 'HOST-RESOURCES-MIB::hrProcessorLoad.'+str(i+199608))[0].split(' ')[3].strip()
    #     print(temp)
    #     cpu=cpu+int(temp)
    # cpu = round(float(cpu/num_process),2)
    cpuload=cpuload[0].split(':')[3].strip()
    return cpuload
# ------------------------------------------------------------
# 获取负载信息
# ------------------------------------------------------------


def getLoad(host, loid):
    """系统负载"""
    load_oids = '1.3.6.1.4.1.2021.10.1.3.' + str(loid)
    return snmpWalk(host, load_oids)[0].split(':')[3]


def getLoads(host):
    load1 = getLoad(host, 1)
    load10 = getLoad(host, 2)
    load15 = getLoad(host, 3)
    return load1, load10, load15

# ------------------------------------------------------------

# ------------------------------------------------------------
# 获取网卡流量
# ------------------------------------------------------------



def getNetworkDevices(host):
    """获取网络设备信息"""
    device_mib = snmpWalk(host, 'RFC1213-MIB::ifDescr')
    device_list = []
    for item in device_mib:
        device_list.append(item.split(':')[3].strip())
    return device_list


def getNetworkData(host, oid):
    """获取网络流量"""
    data_mib = snmpWalk(host, oid)
    data = []
    for item in data_mib:
        byte = float(item.split(':')[3].strip())
        data.append(str(round(byte / 1024, 2)) + ' KB')
    return data

@eel.expose
def getNetworkInfo(host):
    device_list = getNetworkDevices(host)
    # 流入流量
    inside = getNetworkData(host, 'IF-MIB::ifInOctets')
    # 流出流量
    outside = getNetworkData(host, 'IF-MIB::ifOutOctets')
    print(inside+outside)
    return device_list, inside, outside

# ------------------------------------------------------------


# ------------------------------------------------------------
# 内存使用率
# ------------------------------------------------------------

def getSwapTotal(host):
    swap_total = snmpWalk(host, 'UCD-SNMP-MIB::memTotalSwap.0')[0].split(' ')[3]
    return swap_total


def getSwapUsed(host):
    swap_avail = snmpWalk(host, 'UCD-SNMP-MIB::memAvailSwap.0')[0].split(' ')[3]
    swap_total = getSwapTotal(host)
    swap_used = str(round(((float(swap_total) - float(swap_avail)) / float(swap_total)) * 100, 2)) + '%'
    return swap_used


def getMemTotal(host):
    mem_total = snmpWalk(host, 'UCD-SNMP-MIB::memTotalReal.0')[0].split(' ')[3]
    return mem_total


def getMemUsed(host):
    mem_total = getMemTotal(host)
    mem_avail = snmpWalk(host, 'UCD-SNMP-MIB::memAvailReal.0')[0].split(' ')[3]
    mem_used = str(round(((float(mem_total) - float(mem_avail)) / float(mem_total)) * 100, 2)) + '%'
    return mem_used


def getMemInfo(host):
    mem_used = getMemUsed(host)
    swap_used = getSwapUsed(host)
    return mem_used, swap_used

# ------------------------------------------------------------
@eel.expose
def getData():
    host='192.168.138.128'
    data={}
    data['CPU']=int(getCPU(host))
    mem_used, _ = getMemInfo(host)
    mem_used=mem_used.strip('%')
    data['MEM']=float(mem_used)
    _, inside, outside = getNetworkInfo(host)
    data['netin']=getNum(inside[1])
    data['netout']=getNum(outside[1])
    #print(json.dumps(data))
    #with open('data.js','w') as f:
    #    f.write('var myData = ['+ json.dumps(data)+'];')
    return data

@eel.expose
def getDiskuse():
    host='192.168.138.128'
    disk_use=snmpWalk(host,'.1.3.6.1.4.1.2021.9.1.7')
    newdisk=[]
    for disk in disk_use:
        disk= '%.2f GB' % (int(disk.split(' ')[-1])/1024/1024)
        newdisk.append(disk)
    #print(newdisk)
    return(newdisk)

@eel.expose
def getDisktotal():
    host='192.168.138.128'
    disk_total=snmpWalk(host,'.1.3.6.1.4.1.2021.9.1.6')
    #print(disk_total)
    newdisk=[]
    for disk in disk_total:
        disk= '%.2f GB' % (int(disk.split(' ')[-1])/1024/1024)
        newdisk.append(disk)
    print(newdisk)
    return(newdisk)

@eel.expose
def getNum(str):
    str1 = str.rstrip(' KB')
    str1 = float(str1)
    return str1


def main():
    for host in hosts:
        print('=' * 10 + host + '=' * 10)
        start = time.time()
        print("系统信息")
        system = getSystem(host)
        print(system)

        print("系统负载")
        load1, load10, load15 = getLoads(host)
        print('load(5min): %s ,load(10min): %s ,load(15min): %s' % (load1, load10, load15))
        print (getCPU(host))
        print("网卡流量")
        device_list, inside, outside = getNetworkInfo(host)
        for i, item in enumerate(device_list):
            print('%s : RX: %-15s   TX: %s ' % (device_list[i], inside[i], outside[i]))

        mem_used, swap_used = getMemInfo(host)
        print("内存使用率")
        print('Mem_Used = %-15s   Swap_Used = %-15s' % (mem_used, swap_used))

        end = time.time()
        print('run time:', round(end - start, 2), 's')




if __name__ == '__main__':
    # getDiskuse()
    getDisktotal()
    # getNetworkInfo('127.0.0.1')
    #eel.init('test')
    #eel.start('index.html')
    # cpuload=snmpWalk('192.168.138.128', '1.3.6.1.4.1.2021.11.11.0')
    # i = snmpWalk('192.168.138.128', 'HOST-RESOURCES-MIB::hrProcessorLoad.'+str(199609))
    # print(cpuload)
    # print(i)

