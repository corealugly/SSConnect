#!/bin/python2.7
import paramiko
import socket
import csv
import re
import argparse
import sys
import os

# def createLock():
#     with


def eprint(arg):
    print >> sys.stderr, arg

def listStrip(list):
    locallist=[]
    for id in list:
        locallist.append(id.strip())
    return locallist

1
def Phosts(Lhosts):
    for idy in Lhosts.split("\n"):
        # result = re.match(r"#", idy)
        # if not (re.match(r"#", idy)):
        regular = re.compile(r'(?P<ip>^[ \t]*\d+.\d+.\d+.\d+){1}([\t ]+(?:(?!\d+.\d+.\d+.\d+)\w+[\.\-]{0,1})+)+$')
        result = regular.match(idy)
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

lock_path = __file__ + ".lock"

def main():
    global lock_path
    parser = argparse.ArgumentParser(description='SSConnect')
    # parser.add_argument('-p', '--password', type=str, help='enter password')
    parser.add_argument('--lock', type=str, help='lock file')       ##default initialize out main()
    parser.add_argument('--ip', type=str, help='input csv file with ip', required=True)
    parser.add_argument('--login', type=str, help='input csv file with login', required=True)
    parser.add_argument('--password', type=str, help='input csv file with pass', required=True)
    parser.add_argument('--output', type=str, help='output csv file')
    parser.add_argument('-p','--port', type=int, default=22,help='port')
    parser.add_argument('-t', '--timeout', type=int, default=2, help='timeout')

    args = parser.parse_args()
    if len(sys.argv) == 0:
        parser.print_help()
        exit(1)

    if args.lock:
        lock_path = args.lock

    ipf = open(args.ip, 'r')
    varip = listStrip(ipf.readlines())
    ipf.close()

    logf = open(args.login, 'r')
    varlogin = listStrip(logf.readlines())
    logf.close()

    passf = open(args.password, 'r')
    varpass = listStrip(passf.readlines())
    passf.close()

    if args.output:
        outfile = open(args.output, 'w')
        writeF = csv.writer(outfile, delimiter=";")
    else:
        writeF = csv.writer(sys.stdout, delimiter=";")

    eprint(varip)
    eprint(varlogin)
    eprint (varpass)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for idip in varip:
        # if not  (TestConnect(idip,22,0.1)):
        #     print "host down"
        #     continue
        for idl in varlogin:
            for idp in varpass:
                try:
                    client.connect(hostname=idip, username=idl, password=idp, port=args.port) #port_connect, timeout=timeout_tcp )
                    stdin, stdout, stderr = client.exec_command('cat /etc/hosts')
                    data = stdout.read() + stderr.read()
                    # Phosts(data)
                    # print ("good connect to %s 'SSH'" % (idip))
                    writeF.writerow([idip, idl, idp])
                except paramiko.BadHostKeyException as e:
                    writeF.writerow([idip, "", "", "bad_host_key"])
                except paramiko.AuthenticationException as e:
                    # print "auth error -- ip: {0} login: {1} pass: {2} error: {3}".format(idip,idl,idp, e)
                    writeF.writerow([idip,idl,idp,"bad_auth"])
                except paramiko.ssh_exception.NoValidConnectionsError as e:
                    # print "ssh except"
                    # continue
                    writeF.writerow([idip, idl, idp, "bad connect"])



    # data = stdout.read() + stderr.read()
    # print stdout.read()
    # outfile = open(outfilepath,'w')
    # outfile.write(stdout.read())
    # outfile.close()

# from ansible.module_utils.basic import *

if __name__ == "__main__":
    code = 0
    try:
        main()
    except Exception as ex:
        eprint(ex.message)
        code = -1
    except:
        eprint('unknown exception')
        code = -2
    # finally:
    try:
        with open(lock_path, "w") as lck:
            lck.write(str(code))
    except Exception as err:
         eprint(err)
    exit(code)


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