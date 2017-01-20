#!/bin/bash

source ./pt-19637-openrc.sh

cd ./ansible

echo "Deleting all existing instances and provisioning new instances on Nectar."

ansible-playbook -i hosts local_action.yml

if [ $? -eq 0 ]
then
  echo "Successfully provision Nectar instances. Hosts file is updated with new hosts."
else
  echo "Provision Failed." >&2
  exit 1
fi

ansible-playbook -i hosts remote_action.yml