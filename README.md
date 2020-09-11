- [EX284 preparation](#ex284-preparation)

- [EX284 preparation](#ex284-preparation)
- [EX447 preparation](#ex447-preparation)
  - [Git](#git)
  - [Manage inventory variables](#manage-inventory-variables)
  - [Lookup](#lookup)
    - [Lookiup in CSV](#lookiup-in-csv)
  - [Filters and testing and network](#filters-and-testing-and-network)
    - [Create users based on json, using filters](#create-users-based-on-json-using-filters)
    - [Using wilter with  network address](#using-wilter-with-network-address)
  - [Delegation](#delegation)
  - [Dynamic inventory](#dynamic-inventory)
  - [Launch job with API](#launch-job-with-api)

# EX284 preparation 
RHCE preparation files

# EX447 preparation
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

```
 Debug output variables - var_debug.yml:
 ansible-playbook -i inventory3 var_debug.yml
```

## Lookup

https://liquidat.wordpress.com/2016/02/09/howto-looking-up-external-directories-in-ansible/

### Lookiup in CSV

Use following CSV sample file: gamma.csv
groupname,port,enabled
webserevers,8080,yes
webserevers,80,yes
dbservers,8080,no
dbservers,80,no

Create enable_ports.yml file, which will loop trough CSV file and enable ports specified ports in specific group.

    ---
    - name: demo lookups
      hosts: all
      tasks:
        - name: lookup of a csv file
          debug: msg="{{ lookup('csvfile','webservers file=gamma.csv delimiter=, col=2') }}"



## Filters and testing and network
https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html
https://docs.ansible.com/ansible/latest/user_guide/playbooks_tests.html
https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters_ipaddr.html

### Create users based on json, using filters
Create filter_users.yml file.

Use following variable:

    - usersonhosts: {
      userlist: [
        {
        name: "alice",
        group: "ws",
        uid: 1201
      },
      {
        name: "vincent",
        group: "ws",
        uid: 1202
      },
      {
        name: "sandy",
        group: "db",
        uid: 2201
      },
      {
        name: "patrick",
        group: "db",
        uid: 2202
      }
      ]
    }

Create users on ws or db servers based on groups. Use filter function and lookup.

### Using wilter with  network address

Show public network IPV4 address , use ip filter 


## Delegation

Docs: https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html

Create new rolling_update.yml file, with folowing steps:

1. run activity on 50% of webservers
2. take out these servers from proxy pool (user any list, e.g /etc/serverlist )
3. deploy new content (html or any other file)
4. take server back to pool

## Dynamic inventory

Docs: https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#inventory-source-common-format

Implement python file with dynamic inventory (inventory4.py) to sample structure of iunventory with webservers and proxy. Include also some vars, e.g. remote_user. 
Use such file also as dynamic inventory with ansible tower deployment.

Also can be used in ansible command or with playbook:

    ansible -i inventory4.py all -m ping 


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

Example of dynamic inventory using mysql:
https://github.com/askdaddy/ansible-dynamic-inventory-mysql/blob/arya/inventory.py

## Launch job with API

Docs: https://docs.ansible.com/ansible-tower/2.4.5/html/towerapi/intro.html

Get info about to run: https://192.168.1.23/api/v2/job_templates/11/launch/

Create playbook uri_launch.yml to launch project update (e.g. project 10) and start job template  (e.g. id 11) on your tower host.

example:


    - name: start job template
      uri:
        url:  "https://{{towerhost}}/api/v2/job_templates/{{towerjob}}/launch/"
        method: POST
        user: "{{toweruser}}"
        password: "{{towerpass}}"
        validate_certs: False
        force_basic_auth: yes
        status_code:
          - 200
          - 201
          - 202
      register: response
      changed_when: response.status == 201

More examples: https://www.ansible.com/blog/getting-started-ansible-towers-api

e.g.

    name: kick off the provisioning job template
      shell:  "curl -f -H 'Content-Type: application/json' -XPOST --user 
    admin:{{ towerpass }} 
    https://192.168.1.23/api/v2/job_templates/11/launch/ --insecure"
      when: inventory_hostname == 'demovm4'


