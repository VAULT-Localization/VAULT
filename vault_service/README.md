# VAULT Service

Guide to create a Linux service to execute VAULT:

1. Copy files

```shell
$ sudo cp vault.sh /usr/local/bin/vault.sh
$ sudo cp vault.service /etc/systemd/system/vault.service
```

2. Add permissions

```shell
$ sudo chmod 744 /usr/local/bin/vault.sh
$ sudo chmod 664 /etc/systemd/system/vault.service
```

3. Create environment file

```shell
$ sudo touch /etc/vault
```

4. Edit the environment variables of /etc/vault

5. Enable and start the service

```shell
$ sudo systemctl daemon-reload
$ sudo systemctl enable vault.service
$ sudo service vault start
```

6. Check the service status

```shell
$ sudo service vault status
```
