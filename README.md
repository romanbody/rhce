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
** ansible1
** ansible2
* proxy
** ansible3
* dbserver
** ansible4
** ansible5
* test 
** ansible4
* production
** ansible5



Define variables based on:
* groups
* hosts (multiple files?)

Hosts in webserer group will use following variable with list of packages:
* req_packages
** httpd

Hosts in dbserver group will use following variable with list of packages:
* req_packages
** portsgresql

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

