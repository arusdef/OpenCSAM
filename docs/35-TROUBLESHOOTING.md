# Troubleshooting

## System Components

1. [NGINX](https://www.nginx.com/)
1. [Jenkins](https://jenkins.io/)
1. [Kibana](https://www.elastic.co/products/kibana)
1. [Elasticsearch](https://www.elastic.co/products/elasticsearch)

Please, see [architecture](./15-ARCHITECTURE.md) documentation on where each of those components is running. Then you can ssh to the node and debug the issue.

Most of the components are run with [systemd](https://www.freedesktop.org/wiki/Software/systemd/) which is a linux service manager.

Here, I'll use NGINX as an example, but the same techniques can be applied to other components.

## Failure Playbook

### SSH to the remote server

```sh
ssh 139.91.221.81 -l root
```

Type in the password on request.

### Check Service Status

```sh
systemctl status nginx

● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2018-07-09 18:26:46 EEST; 2 weeks 2 days ago
  Process: 29871 ExecReload=/bin/kill -s HUP $MAINPID (code=exited, status=0/SUCCESS)
 Main PID: 1639 (nginx)
    Tasks: 4
   Memory: 17.7M
   CGroup: /system.slice/nginx.service
           ├─ 1639 nginx: master process /usr/sbin/nginx
           ├─20935 nginx: worker process is shutting down
           ├─29873 nginx: worker process
           └─29874 nginx: worker process

Jul 16 15:41:23 CSAM-Zeus systemd[1]: Reloaded The nginx HTTP and reverse proxy server.
```

The state of the service should be `active (running)`. Also, you can see a few lines of very latest logs.

### Service Restart

```sh
systemctl restart nginx # to stop and start the process
systemctl reload nginx # to remain running, but reload configuration
```

Alternatively, you can stop and start the service manually

```sh
systemctl stop nginx # to stop the process
systemctl start nginx # to start the process
```

### Service Logs

There is a journalctl service is running on each machine

```sh
journalctl # to see all logs
journalctl -u nginx # to see nginx logs
journalctl -u nginx --lines=100 # to see last 100 lines of nginx logs
journalctl -u nginx -f # to follow nginx logs, brake with ctrl-c
```

Sometimes logs (or some specific logs) can be found in `/var/log/--service name--`.

```sh
ls -lA /var/log/nginx/

-rw-r--r--. 1 nginx nginx 727357 Jul 26 16:04 access.log
-rw-r--r--. 1 nginx nginx  33673 Jul 26 00:20 access.log-20180726.gz
-rw-r--r--. 1 nginx nginx   7424 Jul 26 14:42 error.log
-rw-r--r--. 1 nginx nginx   1269 Jul 25 18:48 error.log-20180726.gz
```

So, for the current nginx example there are logs which nginx does not write to `journald` but `/var/log/nginx`. Here you can see all access requests and access errors.