# gecoshc-server
Help Channel Server deployment and configuration for GECOS integration.

This project is basically a noVNC + UVNC Repeater server to allow technical support to GECOS workstations.
GECOS workstations users may use a VNC client to connect to  the UVNC Repeater server and the technical support person may use noVNC to manage the VNC session of the user.

The UVNC Repeater server has been modified to validate the IDs against the GECOS Control Center.

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

After installing you will need to restart the computer or start the services manually:
```
/etc/init.d/nginx start
/etc/init.d/gecoshc_repeater start
/etc/init.d/gecoshc_ws_client start
/etc/init.d/gecoshc_ws_server start
```

Probably you will also need to open the SSL port (443) in your firewall.

# Configuring
After installing is important to configure the GECOS CC address in the UVNC repeater server.
If the GECOS CC address is not configured the system will work fine but the IDs will not be validated. That means that your installation will be at risk since anybody can use it.

To configure the GECOS CC address edit the start script called "gecoshc_repeater" and add "-g https://gecoscc.yourdomain.com" to PROGRAM_OPTS.

```
/etc/init.d/gecoshc_repeater stop
sed -i 's|PROGRAM_OPTS="-d -l $LOGS"|PROGRAM_OPTS="-d -l $LOGS -g https://gecoscc.yourdomain.com"|g' /etc/init.d/gecoshc_repeater 
/etc/init.d/gecoshc_repeater start
```

If your SSL certifcate is not valid you may have to set PERL_LWP_SSL_VERIFY_HOSTNAME environment variable to 0 (it depends on your Perl version).

The GECOS workstation user must start the Help Channel client and the technical support person must open the noVNC site in is browser in less than 5 minutes. This timeout is configured in /etc/gecos/helpchannel/nginx.conf:

```
# Connection timeout
proxy_read_timeout     300;
proxy_connect_timeout  300;
```





