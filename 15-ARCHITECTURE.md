# Cluster Architecture

## Architecture Componenets

| Service Name      | Public IP     | Private IP    | Ports         |
| :-----------------|--------------:|--------------:|--------------:|
| Nginx             | 139.91.221.81 | 172.16.221.81 | 443           |
| Jenkins           | 139.91.221.82 | 172.16.221.82 | 8080          |
| Kibana            | 139.91.221.82 | 172.16.221.82 | 5601          |
| Webapp            | 139.91.221.82 | 172.16.221.82 | 4200          |
|                   | 139.91.221.83 | 172.16.221.83 |               |
| Elasticsearch     | 139.91.221.84 | 172.16.221.84 | 9200, 9300    |
| Elasticsearch     | 139.91.221.85 | 172.16.221.85 | 9200, 9300    |
| Elasticsearch     | 139.91.221.86 | 172.16.221.86 | 9200, 9300    |
| Elasticsearch     | 139.91.221.87 | 172.16.221.87 | 9200, 9300    |

### References

1. [NGINX](https://www.nginx.com/)
1. [Jenkins](https://jenkins.io/)
1. [Kibana](https://www.elastic.co/products/kibana)
1. [Elasticsearch](https://www.elastic.co/products/elasticsearch)

### Reverse Proxy

NGINX is acting as a reverse proxy for all other services (Jenkins, Kibana, ES, UI). You can think of it as an entrypoint to the system. Currently, NGINX is configured to proxy traffic for these domain names.

1. https://kibana.opencsam.enisa.europa.eu/
1. https://elastic.opencsam.enisa.europa.eu/
1. https://jenkins.opencsam.enisa.europa.eu/
1. https://webapp.opencsam.enisa.europa.eu/

Currently, these domain names are not public (not A records) and so should be configured either locally (updating your `/etc/hosts` file) or on a local DNS server.

### Local Configuration

You need to tell your computer on how to map DNS name to a specific IP address. It can be done by editing your local `/etc/hosts` file.

#### Mac users

You can open the terminal and just run this script.

```sh
sudo bash -c 'for s in "" "139.91.221.81 webapp.opencsam.enisa.europa.eu" "139.91.221.81 elastic.opencsam.enisa.europa.eu" "139.91.221.81 jenkins.pencsam.enisa.europa.eu" "139.91.221.81 kibana.opencsam.enisa.europa.eu"; do echo $s >> /etc/hosts; done'
```

If it doesn’t work for whatever reason you can run ```sudo vi /etc/hosts``` from the terminal and add these lines to the very end of the file.

```s
139.91.221.81   webapp.opencsam.enisa.europa.eu
139.91.221.81   elastic.opencsam.enisa.europa.eu
139.91.221.81   jenkins.opencsam.enisa.europa.eu
139.91.221.81   kibana.opencsam.enisa.europa.eu
```

#### Windows users

You need to edit /etc/hosts file as well. Basically, you need to add these lines in there. Unfortunately, it’s a bit more complex on Windows because of different Windows versions and configurations. Please, see a [tutorial](https://gist.github.com/zenorocha/18b10a14b2deb214dc4ce43a2d2e2992)

```s
139.91.221.81   webapp.opencsam.enisa.europa.eu
139.91.221.81   elastic.opencsam.enisa.europa.eu
139.91.221.81   jenkins.opencsam.enisa.europa.eu
139.91.221.81   kibana.opencsam.enisa.europa.eu
```
