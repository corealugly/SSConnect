#!/bin/python2.7
import paramiko
import socket
import csv
import re

from cryptography import exceptions


def Wopen(filepath, type):
    try:
        return open(filepath, type)
    except:
        print "no file exist"
        return False

def listStrip(list):
    locallist=[]
    for id in list:
        locallist.append(id.strip())
    return locallist

# def strStrip(str):
#     localstr=""

def Phosts(Lhosts):
    for idx,idy in enumerate(Lhosts.split("\n")):
        # result = re.match(r"#", idy)
        # if not (re.match(r"#", idy)):
        result = re.compile(r'(?P<ip>^[ \t]*\d+.\d+.\d+.\d+){1}([\t ]+(?:(?!\d+.\d+.\d+.\d+)\w+[\.\-]{0,1})+)+$')

        if result:
            print idy
        # print str(idx) + " : " + idy


def TestConnect(ip, port, timeout, file=None):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip,port))
    except Exception as e:
        print("something's wrong with %s. Exception is %s" % (ip,e))
        return False
    else:
        print ("good connect to {0} 'SOCKET'".format(ip))
        return True
    finally:
        # print "socket close!\n",
        s.close()


def main():

    ipfilepath='/home/corealugly/ip.txt'
    loginfilepath='/home/corealugly/login.txt'
    passfilepath='/home/corealugly/pass.txt'
    outfilepath='/home/corealugly/out.txt'
    outbadfilepath = '/home/corealugly/bad_out.txt'
    host = ''
    user = ''
    secret = ''
    port_connect = 22
    timeout_tcp = 2

    ipfilepath = Wopen(ipfilepath, 'r')
    varip = listStrip(ipfilepath.readlines())
    ipfilepath.close()

    infilelogin = Wopen(loginfilepath, 'r')
    varlogin = listStrip(infilelogin.readlines())
    infilelogin.close()

    infilepass = Wopen(passfilepath, 'r')
    varpass = listStrip(infilepass.readlines())
    infilepass.close()

    outfileG = Wopen(outfilepath, 'w')
    writeFG = csv.writer(outfileG, delimiter=";")

    outfileB = Wopen(outbadfilepath, 'w')
    writeFB = csv.writer(outfileB, delimiter=";")

    # print varip
    # print varlogin
    # print varpass

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(hostname =host, username=user, password=secret, port=22)
    for idip in varip:
        # if not  (TestConnect(idip,22,0.1)):
        #     print "host down"
        #     continue
        for idl in varlogin:
            for idp in varpass:
                try:
                    client.connect(hostname=idip, username=idl, password=idp, port=22) #port_connect, timeout=timeout_tcp )
                    stdin, stdout, stderr = client.exec_command('cat /etc/hosts')
                    data = stdout.read() + stderr.read()
                    Phosts(data)
                    # print ("good connect to %s 'SSH'" % (idip))
                    writeFG.writerow([idip, idl, idp])
                except paramiko.BadHostKeyException as e:
                    writeFG.writerow([idip, "", "", "bad_host_key"])
                except paramiko.AuthenticationException as e:
                    # print "auth error -- ip: {0} login: {1} pass: {2} error: {3}".format(idip,idl,idp, e)
                    writeFB.writerow([idip,idl,idp,"bad_auth"])
                except paramiko.ssh_exception.NoValidConnectionsError as e:
                    # print "ssh except"
                    continue
                    writeFB.writerow([idip, idl, idp, "bad connect"])



    # data = stdout.read() + stderr.read()
    # print stdout.read()
    # outfileG = Wopen(outfileGpath,'w')
    # outfileG.write(stdout.read())
    outfileG.close()
    outfileB.close()


# from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()

'''
if __name__ == "__main__":
    # main()
    # module = AnsibleModule(
    #     argument_spec=dict(
    #         hosts = dict(type='str', required=True),
    #         creds = dict(type='str', required=True)
    #     )
    # )
    dc = {}
    dc["arg1"] = "val of arg1"
    dc["arg2"] = 13
    #print(**dc) # -> print(ab="cd", 12=13)
    def myfunk(arg1=0, arg2=0):
        print("arg1:", arg1, "arg2:", arg2)
    myfunk(**dc)
'''