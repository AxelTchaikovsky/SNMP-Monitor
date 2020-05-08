import os
from easysnmp import snmp_walk

def oid():
    host = '127.0.0.1'
    oid = input('Please input OID:\n')
    result=os.popen('snmpwalk -v 2c -c public '+host+' '+oid).read()
    print(result)


def traporset():
    host = '127.0.0.1'
    oid = input('Trap or Set(Please input T or S):\n')
    if oid=='T':
        result=os.popen("sudo snmptrap -v1 -c public localhost 1.3.6.1.4.1.1 10.10.12.219 2 3 1000 1.3.6.1.9.9.44.1.2.1 i 12 1.3.4.1.2.3.1 s hi,imhere").read()
        print(result)
    elif oid=='S':
        session = Session(hostname='localhost', community='private', version=2)
        # Set a variable using an SNMP SET
        session.set('SNMPv2-MIB::sysName.0', 'The SNMP Lab')
        result = session.get('SNMPv2-MIB::sysName.0')
        print(result)

    else:
        print("Wrong input!")
    


if __name__=='__main__':
    word = input("oid or trap/set\n 1 oid\n 2 trap/set\n please input [1/2]:")
    if word=='1':
        oid()
    elif word=='2':
        traporset()
    else:
        print("Wrong input!")
