#!/bin/python2.7
import paramiko
import socket

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
        print "socket close!\n",
        s.close()


def main():

    ipfilepath='/home/corealugly/ip.txt'
    loginfilepath='/home/corealugly/login.txt'
    passfilepath='/home/corealugly/pass.txt'
    outfilepath='/home/corealugly/out.txt'
    host = ''
    user = ''
    secret = ''
    port = 22

    ipfilepath = Wopen(ipfilepath, 'r')
    varip = listStrip(ipfilepath.readlines())


    infilelogin = Wopen(loginfilepath, 'r')
    varlogin = listStrip(infilelogin.readlines())

    infilepass = Wopen(passfilepath, 'r')
    varpass = listStrip(infilepass.readlines())

    print varip
    print varlogin
    print varpass

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(hostname =host, username=user, password=secret, port=22)
    for idip in varip:
        if not  (TestConnect(idip,22,1)):
            print "host down"
            continue
        for idl in varlogin:
            for idp in varpass:
                try:
                    client.connect(hostname=host, username=idl, password=idp, port=22 )
                    stdin, stdout, stderr = client.exec_command('cat /etc/hosts')
                except Exception as e:
                    print "auth error -- ip: {0} login: {1} pass: {2} error: {3}".format(idip,idl,idp,e)
                else:
                    print ("good connect to %s 'SSH'" % (idip))



    # data = stdout.read() + stderr.read()
    # print stdout.read()
    # outfile = Wopen(outfilepath,'w')
    # outfile.write(stdout.read())
    # outfile.close()

if __name__ == "__main__":
    main()