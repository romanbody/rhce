#!/usr/bin/env python3.6

from subprocess import Popen, PIPE
import sys
import json

result = {}

result['all'] = {}
result['all']['hosts'] = ['localhost']
result['all']['vars'] = {}

result['webservers'] = {}
result['webservers']['hosts'] = ['ansible1','ansible2']
result['webservers']['vars'] = {}

result['proxy'] = {}
result['proxy']['hosts'] = ['ansible3','localhost']
result['proxy']['vars'] = {}


if len(sys.argv) == 2 and sys.argv[1] == '--list':
    print(json.dumps(result))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    print(json.dumps({'remote_user': 'ansible'}))
else:
    sys.stderr.write("Need an argument, either --list or --host <host>\n")
