- [EX284 preparation](#ex284-preparation)
- [EX447](#ex447)
  - [Git](#git)
  - [Manage inventory variables](#manage-inventory-variables)
  - [Lookup](#lookup)
  - [https://liquidat.wordpress.com/2016/02/09/howto-looking-up-external-directories-in-ansible/](#httpsliquidatwordpresscom20160209howto-looking-up-external-directories-in-ansible)
  - [Filters and testing and network](#filters-and-testing-and-network)
  - [Delegation](#delegation)
  - [Dynamic inventory](#dynamic-inventory)
  - [Lunch job with API](#lunch-job-with-api)

# EX284 preparation 
rhce preparation files

# EX447
Ex447 preparation files

## Git
git clone, commit, push, pull etc.

## Manage inventory variables

Define inventory:
* ansible1
* ansible2
* ansible3
* ansible4
* ansible5

With groups:
* webserver
  * ansible1
  * ansible2
* proxy
  * ansible3
* dbserver
  * ansible4
  * ansible5
* test 
  * ansible4
* production
  * ansible5



Define variables based on:
* groups
* hosts 

Hosts in webserer group will use following variable with list of packages:
* req_packages
  * httpd

Hosts in dbserver group will use following variable with list of packages:
* req_packages
  * portsgresql

All hosts will use following variable:
* motd_welcome

Ansible4 as db test server will have following variables:
* open_ports
* open_hosts

Ansible5 as db production server will have following variables:
* open_ports
* open_hosts

Use special variables:
* define ansible5 host with specific connection - IP and custom user name for db production server

## Lookup

https://liquidat.wordpress.com/2016/02/09/howto-looking-up-external-directories-in-ansible/
---
- name: demo lookups
  hosts: neon
tasks:
    - name: lookup of a csv file
      debug: msg="{{ lookup('csvfile','dinner file=gamma.csv delimiter=, col=2') }}"


## Filters and testing and network
https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html
https://docs.ansible.com/ansible/latest/user_guide/playbooks_tests.html
https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters_ipaddr.html

## Delegation
https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html

## Dynamic inventory
https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#inventory-source-common-format

Example:
#!/usr/bin/env python

from subprocess import Popen, PIPE
import sys
import json

result = {}
result['all'] = {}

result['all']['hosts'] = ['localhost']
result['all']['vars'] = {}

if len(sys.argv) == 2 and sys.argv[1] == '--list':
    print(json.dumps(result))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    print(json.dumps({'ansible_connection': 'jail'}))
else:
    sys.stderr.write("Need an argument, either --list or --host <host>\n")

## Lunch job with API
https://docs.ansible.com/ansible-tower/2.4.5/html/towerapi/intro.html

https://172.17.53.212/api/

Get info about to run
https://172.17.53.212/api/v2/job_templates/11/launch/

https://www.ansible.com/blog/getting-started-ansible-towers-api
- name: kick off project sync
  uri:
    url:  https://localhost/api/v1/projects/7/update/
    method: POST
    user: admin
    password: "{{ towerpass }}"
    validate_certs: False
    status_code:
      - 200
      - 201
      - 202
  when: response.status == 201

From <https://www.ansible.com/blog/getting-started-ansible-towers-api> 

name: kick off the provisioning job template
  shell:  "curl -f -H 'Content-Type: application/json' -XPOST --user 
admin:{{ towerpass }} 
https://172.16.2.42/api/v2/job_templates/8/launch/ --insecure"
  when: inventory_hostname == 'demovm4'

From <https://www.ansible.com/blog/getting-started-ansible-towers-api> 
