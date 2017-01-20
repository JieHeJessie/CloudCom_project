from novaclient import client
import os
import time
import os.path

def get_nova_obj():
  return client.Client("2", os.environ['OS_USERNAME'], os.environ['OS_PASSWORD'], os.environ['OS_PROJECT_NAME'], os.environ['OS_AUTH_URL'])

def get_servers(nova):
  return nova.servers.list()

def create_server(nova,instance_name,image_id,image_flavor,key_name,security_group_names):
  security_groups = find_security_groups(security_group_names)
  return nova.servers.create(instance_name, image_id, image_flavor, security_groups=security_groups, key_name=key_name)

def get_ipaddr(nova,server_id):
  count_retry=0
  while(count_retry < 60):
    server=nova.servers.find(id=server_id)
    if len(server.addresses) > 0:
      if len(server.addresses.values()[0]) > 0:
        ipaddr = server.addresses.values()[0][0][u'addr']
        if ipaddr:
          return ipaddr
    count_retry += 1
    time.sleep(2)
  raise Exception("Can't get IP for this server. You sure it's right?")
  
def provision_server(instance_name,image_id,image_flavor,key_name,security_group_names):
  nova = get_nova_obj()
  server= create_server(nova,instance_name,image_id,image_flavor,key_name,security_group_names)
  return get_ipaddr(nova,server.id)

def find_security_groups(security_group_names):
  nova = get_nova_obj()
  groups=nova.security_groups.list()
  names=security_group_names.split(",")
  security_group_ids = []
  for group in groups:
    for name in names:
      if group.name == name:
        security_group_ids.append(group.id)
  return security_group_ids

def delete_all_servers():
  nova = get_nova_obj()
  servers = get_servers(nova)
  for server in servers:
    print "Terminating server {0} ({1})".format(server.name, server.id)
    server.delete()

def create_tomcat_security_group():
  nova = get_nova_obj()
  
  existing_group = nova.security_groups.find(name="tomcat")

  if existing_group:
    existing_group.delete()

  time.sleep(10)

  group = nova.security_groups.create("tomcat","Port 8080")
  time.sleep(10)

  nova.security_group_rules.create(group.id, ip_protocol="tcp",from_port=8080,to_port=8080)   

def create_couchdb_security_group():
  nova = get_nova_obj()
  
  existing_group = nova.security_groups.find(name="couchdb")

  if existing_group:
    existing_group.delete()

  time.sleep(10)

  group = nova.security_groups.create("couchdb","Port 5984")
  time.sleep(10)

  nova.security_group_rules.create(group.id, ip_protocol="tcp",from_port=5984,to_port=5986)

def add_keypair(public_key_file_path,keypair_name):
  nova = get_nova_obj()

  with open(os.path.expanduser(public_key_file_path)) as f:
    public_key = f.read()

  nova.keypairs.create(keypair_name,public_key)





  
	

	

