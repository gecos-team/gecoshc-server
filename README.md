# gecoshc-server
Help Channel Server deployment and configuration for an AppImage client.

This project is basically a noVNC + UVNC Repeater server to allow technical support.
Workstations users may use a VNC client to connect to  the UVNC Repeater server and the technical support person may use noVNC to manage the VNC session of the user.

The UVNC Repeater server has been modified to validate the server key comming from the client.

# Relathionship with other projects
This project includes:
* noVNC and websockify (https://novnc.com/)
* A modified version of Karl J. Runge Ultra VNC repeater (http://www.karlrunge.com/x11vnc/ultravnc_repeater.pl)

This project is part of the GECOS environment.

# Building
To build this project just run build_rpm.sh script in CentOS to build a RPM package:
``
./build_rpm.sh
``

# Installing
To install this project use the RPM package by:
``
 yum install gecos-help-channel-server-<version>.noarch.rpm
``

IMPORTANT: Probably you will need to add epel repository to your system before installing gecos-help-channel-server

After installing you will need to restart the computer or start the services manually:
```
 systemctl start nginx
 systemctl start gecoshc_repeater
 systemctl start gecoshc_ws_client
 systemctl start gecoshc_ws_server
```

Probably you will also need to open the SSL port (443) in your firewall.

# Configuring

If your SSL certifcate is not valid you may have to set PERL_LWP_SSL_VERIFY_HOSTNAME environment variable to 0 (it depends on your Perl version).

The user must start the Help Channel client appImage and the technical support person must open the noVNC site in is browser in less than 5 minutes. This timeout is configured in `/etc/gecos/helpchannel/nginx.conf`:

```
# Connection timeout
proxy_read_timeout     300;
proxy_connect_timeout  300;
```

## Default server key

The rpm package puts the server key in /etc/hcpass being the default key: `changeme`.
This key must be changed after the installation.
