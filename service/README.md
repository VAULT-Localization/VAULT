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

4. Add environment variables to /etc/vault

   - ROS 2 config:

     - ROS_DOMAIN_ID
     - RMW_IMPLEMENTATION

   - Ntrip server config

     - NTRIP_HOST
     - NTRIP_PORT
     - NTRIP_MOUNTPOINT
     - NTRIP_USER
     - NTRIP_PASSWORD

   - Sensors config:

     - PUBLISH_T265_ODOM_TF
     - PUBLISH_D435i_IMU_FILTER

   - Visual SLAM config:
     - PUBLISH_VISUAL_SLAM_TF
     - USE_T265
     - USE_GPS
   - EKF config:

     - RUN_EKF
     - RUN_DUAL_EKF

   - Visual odometry config:
     - RUN_RDGD_ODOMETRY
     - RUN_STEREO_ODOMETRY
     - RUN_ICP_ODOMETRY

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
