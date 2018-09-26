# Cluster Setup

## Introduction

The project contains ansible scripts used for automated deployment of infrastructure.

## Architecture Components

Scripts below will update the system and install required components. Currently, key components of the system are

1. [Elasticsearch](https://www.elastic.co/products/elasticsearch)
1. [Kibana](https://www.elastic.co/products/kibana)
1. [Jenkins](https://jenkins.io/)
1. [NGINX](https://www.nginx.com/)

For security reasons Nginx is acting as a reverse proxy for Jenkins, Kibana and ES.

## Cluster Overview

![Cluster Overview](./10-CLUSTER-OVERVIEW.png)
![Logical View](./Enisa%20Logical%20Architecture%20-%20prototype.png)


## Prerequisites

Ansible scripts leverage ansible vault to store sensitive variables. To see all values needed to be present in vault check ansible/roles/common/defaults/main.yml for variables starting with vault_. Vault used by this project is committed to repository and can be found in vault/defaults/main.yml - this file is encrypted and ansible requires password for it to be stored in ansible/.vault_password. If new project is started of this one you need to create your own vault (for details see: Ansible Vault). Currently following variables need to be specified in the vault:

vault_proxy_http_auth_users - list of dictionaries with keys: username and password for HTTP authentication through Nginx proxy
vault_server_key - string containing private SSL key
vault_server_crt - string containing server SSL certificate

In order to generate new credentials run the following command. Replace username and password with required credentials.

```sh
printf "john:$(openssl passwd -crypt 123456)n"
```

To create or edit Ansible vault you can use following commands

```sh
ansible-vault create roles/vault/defaults/main.yml
ansible-vault edit roles/vault/defaults/main.yml
```

where encoded ansible-vault YAML file might look like

```text
---

vault_proxy_http_auth_users:
  - { username: "someone", password: "__encoded password__" }

vault_server_key: |
  -----BEGIN RSA PRIVATE KEY-----
  MIICXgIBAAKBgQC+tKzWu84Q00M4r...
  ...
  ...
  -----END RSA PRIVATE KEY-----

vault_server_crt: |
  -----BEGIN CERTIFICATE-----
  MIICeTCCAeICCQDepvWzdprnjDANB...
  ...
  ...
  -----END CERTIFICATE-----
```

Since SSL is used by Nginx proper SSL certificate/key need to be acquired, see [Generate SSL certificate](#generate-ssl-certificate) for details on creating self-signed certificate yourself.

After above steps ansible can be used to provision server with proper configuration, see Ansible for details.

## Generate SSL Certificate

To generate self-signed SSL certificate run

```sh
openssl genrsa 2048 > host.key
openssl req -new -x509 -nodes -sha1 -days 3650 -key host.key > host.crt
# Use `*.opencsam.enisa.europa.eu` for the Common Name
openssl x509 -noout -fingerprint -text < host.cert > host.info
```

After running above command server.key will contain the private key and server.crt will contain the certificate.

## Ansible Playbooks

Make sure ansible/.vault_password contains proper password for the vault, then run:

If user access is based on credentials.

```sh
cd ansible
# to run all playbooks
ansible-playbook -i hosts.ini deployment.yml -b -v -k
# to run a particular playbook
ansible-playbook -i hosts.ini deployment.yml -b -v -k --tags jenkins
```

If user access is based on a private key.

```sh
cd ansible
# to run all playbooks
ansible-playbook -i hosts.ini deployment.yml -b -v --private-key=~/.ssh/opencsam_rsa
# to run a particular playbook
ansible-playbook -i hosts.ini deployment.yml -b -v --private-key=~/.ssh/opencsam_rsa --tags jenkins
```
