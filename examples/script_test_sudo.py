#!/usr/bin/python3

with open ('/var/log/syslog', 'r') as rf:
    print(rf.read())

