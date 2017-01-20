from invoke import run, task
import nectar
import os

@task
def delete_all_servers():
  """Delete all the existing on Nectar Cloud"""
  nectar.delete_all_servers()

@task
def create_couchdb_security_group():
  """Create CouchDB security group"""
  nectar.create_couchdb_security_group()

@task
def create_tomcat_security_group():
  """Create Tomcat security group"""
  nectar.create_tomcat_security_group()

@task
def add_keypair(public_key_file_path,keypair_name):
  """Add Public Key to the Nectar Cloud to be used later"""
  nectar.add_keypair(public_key_file_path,keypair_name)

@task
def provision_server(instance_name,image_id,image_flavor,key_name,security_group_names):
  """Provision an instance on Nectar Cloud"""
  print nectar.provision_server(instance_name,image_id,image_flavor,key_name,security_group_names)
