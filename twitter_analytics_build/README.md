# Twitter Analytics Project Deployment

This deployment project is used to deploy twitter analytic projects to the Nectar Cloud instances. 

The deployment project is using the following tech stacks:

* **Vagrant**

In order to easily setup and manage all the development dependencies, we use Vagrant box as development environment Virtual. The Vagrant provisioner will run all the scripts inside the */scripts* folder to install ansible package (*ansible.sh*), novaclient(*nova.sh*), python development tools(*python.sh*) so that we can run ansible script, run nova commands, and run python scripts inside the VM. 

The vagrant provisioner creates the /vagrant sync folder. Thus, we can develop in the host machine using our favour dev tools and run the scripts inside the dev environment. 

* **Ansible**

As automation provision tool, Ansible scripts ise used to provision servers and deploy projects to the provisioned servers. 

The whole ansible playbook can be divided into 2 parts. 

The first part is used to create/boot server instances on Nectar Cloud and the server will be dynamically added into inventory hosts. Ansible role server_provision is responsible for this part of job. The playbook used is *ansible/local_action.yml*

The second part is used to install software dependencies and deploy/manage project code into provisioned server instances. The playbook used is *ansible/remote_action.yml*.

* **Python NovaClient**

We leverage the powerful **Python Novaclient** to interact with Nectar OpenStack API. 

All the python scripts for interacting with OpenStack API are located at */ansible/roles/server_provision*. A custom ansible role has been created to allow the provision scripts to delete all the existing instances, upload SSH keypair, create security group and security group rules, and create/boot server instances. 

Moreover, python invoke tasks have been created to easily run the python function. 

## Supported Platforms
The project can be run in MacOS, Windows or Linux 

## Pre-requisites
* Vagrant (https://www.vagrantup.com/)
* Virtual Box (https://www.virtualbox.org/)
* Git

## Startup Development Environment

The Development Environment Virtual Machine will include all the dependencies you need to provision servers on Nectar and deploy projects to the provisioned server. The installed dependencies include:
* Nova
* Ansible
* Python dev tools

Run the following command to startup development environment VM
```
git clone https://bitbucket.org/hejie49/twitter_analytics_build.git
cd twitter_analytics_build
vagrant up --provision
```

## SSH into the Development Environment VM
Once the VirtualBox VM is provisioned, you can run the following command to ssh into the VM:
```
vagrant ssh
```

## Configuration
### Nectar Cloud OpenStack RC File
In order to allow the provision scripts to interact with Nectar Cloud API, we need to leverage the OpenRC file from Nectar Cloud. 
1. Download the OpenStackRC file from the Nectar Cloud.  
(https://support.nectar.org.au/support/solutions/articles/6000078065-api)
1. Copy the RC file to the project root folder (e.g. pt-19637-openrc.sh)
1. Update the go.sh file to source the RC file you downloaded (by replacing ./pt-19637-openrc.sh)

### SSH Key Pair
In order to allow the deployment scripts to clone the project codes from specific repositories and also allow the ansible script to talk to the provisoned server instances, we need to setup and configure SSH key. 

#### Generate SSH Keypair
You can use any existing ssh key or you can generate a new SSH keypair. 
If you would like to generate a new SSH keypair, you can run the following command inside the VM
```
cd ~/.ssh
ssh-keygen
```
Following the prompt, enter the file_name (e.g. id_rsa) you want and press enter directly for the passphase.

#### ansible/local_action.yml for key file location
We need to update the following configration values in the **ansible/local_action.yml**

* *public_key_file_path* the absolute file path of the public key file (e.g., id_rsa.pub)
* *private_key_file_path* the absolute file path of the private key file (e.g., id_rsa)

#### Git Repository and Deployment Key
In order to allow the scripts to download the project code to the instance nodes, we need to upload the deployment public ssh key for each related git repositories. We used the following values in the **ansible/remote_action.yml** file:

* *ssh_deployment_private_key_path* the absolute file path of the private key file for the deployment
* *repo_url_twitter_harvestor* the url of the git repository for twitter harvestor
* *repo_url_web_services* the url of the git repository for web services

#### ansible.cfg
This key pair will also be uploaded to Nectar Cloud to be used between the communication between the Dev VM and new instances. So we need to update the *private_key_file* value in the
the **ansible.cfg** file

# Run the ansible playbook
Now it is time to rock and roll. Run the following command inside the vagrant ssh window:

```
cd /vagrant
./go.sh
```

The command will ask for Nectar Password. Please make sure you read through the document (https://support.nectar.org.au/support/solutions/articles/6000075747-api) to get the Nectar password from the console.




