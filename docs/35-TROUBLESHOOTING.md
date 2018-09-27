# Troubleshooting

## System Components

1. [NGINX](https://www.nginx.com/)
1. [Jenkins](https://jenkins.io/)
1. [Kibana](https://www.elastic.co/products/kibana)
1. [Elasticsearch](https://www.elastic.co/products/elasticsearch)

Please, see [architecture](./15-ARCHITECTURE.md) documentation on where each of those components is running. Then you can ssh to the node and debug the issue.

Most of the components are run with [systemd](https://www.freedesktop.org/wiki/Software/systemd/) which is a linux service manager.

Here, I'll use NGINX as an example, but the same techniques can be applied to other components.

## Change Username or Password

### Pre requirements:

- Open your terminal and go to a empty folder
- Clone the ENISA project:
        - `git clone https://github.com/enisaeu/OpenCSAM`
        - Change to the directory `cd OpenCSAM` and follow the steps in the sections below.

### Change Web Server Username or Password

Make sure that you have `openssl` installed on your machine.

For Mac users it is easy to do with `brew` as

```sh
brew install openssl
```

Then encode the password as

```sh
openssl passwd -apr1
```

Make sure that you are in the project folder and `cd cluster-setup/`.

As a next step you need to edit the `ansible vault` (you will be asked for a vault password)

```sh
ansible-vault edit roles/vault/defaults/main.yml
```

where you should add/modify users credentials in

```text
vault_proxy_http_auth_users:
  - { username: "someone", password: "__encoded password__" }
```

Then just run the ansible playbook to update the nginx configuration (you need ssh password for it)

```sh
ansible-playbook -i hosts.ini deployment.yml -b -v -k --tags nginx
```

Commit `ansible vault` to the git to keep track of all changes.

### Change the Webapp Username or Password:
- Open the file `OpenCSAM/ENISA-UI/app/assets/data.json` in your preffered text editor.
- Change the username or password in the variables `USER_NAME` or `PASSWORD` respectively to the same values used in the `Change Web Server Username or Password`. **Don't modifiy the value of the `ELASTIC_SEARCH_CONTENT_INDEX` variable. Don't modify any other file within the project.**
-  Commit your changes in Git, execute each line below in your terminal:

        `git commit -m "Changed username and password"`
        `git add .` -- is necessary to put the period at the end of this command.
        `git push`

- After the changes have been pushed to the Github:
        
        - Open the link: https://jenkins.opencsam.enisa.europa.eu/job/Enisa%20UI/
        - Click in `Build Now`
        - A progress bar will be presented on the right hand side. The build process takes around 4 minutes to complete.
        - Open the Web App and test the Username or Password change.

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