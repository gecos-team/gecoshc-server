# Copyright: 2018 Junta de Andalucia <gecos@guadalinex.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Name: help-channel-server
Version: 1.0.0
Release: 0

Summary: GECOS - Help Channel Server
License: GPL2
Group: Applications/System
Vendor: GECOS
URL: http://www.juntadeandalucia.es
Packager: Abraham Macias <amacias@solutia-it.es>
Distribution: RHEL 6.0

Source: %{name}-%{version}.tar.gz
BuildArch: noarch

%description
This package provides the Help Channel Server for GECOS environment.

###########################################
%package -n gecos-help-channel-server
###########################################

Summary: GECOS - Help Channel Server
Group: Applications/System
Requires: nginx, openssl, python-websockify, perl-URI, perl-Crypt-SSLeay, perl-IO-Socket-SSL, perl-Proc-Daemon, perl-JSON, redhat-lsb-core, perl-libwww-perl

%description -n gecos-help-channel-server
This package provides the Help Channel Server for GECOS environment.

%prep
%setup -q

%build
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

# install the start scripts
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
install -m 0755 conf/gecoshc_repeater $RPM_BUILD_ROOT/etc/init.d/gecoshc_repeater
install -m 0755 conf/gecoshc_ws_client $RPM_BUILD_ROOT/etc/init.d/gecoshc_ws_client
install -m 0755 conf/gecoshc_ws_server $RPM_BUILD_ROOT/etc/init.d/gecoshc_ws_server

mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -m 0644 conf/gecoshc_repeater.service $RPM_BUILD_ROOT/usr/lib/systemd/system/gecoshc_repeater.service
install -m 0644 conf/gecoshc_ws_client.service $RPM_BUILD_ROOT/usr/lib/systemd/system/gecoshc_ws_client.service
install -m 0644 conf/gecoshc_ws_server.service $RPM_BUILD_ROOT/usr/lib/systemd/system/gecoshc_ws_server.service

mkdir -p $RPM_BUILD_ROOT/var/log/gecos


%post -n gecos-help-channel-server
NXCONFDIR=/etc/nginx/conf.d/
CONFDIR=/etc/gecos/helpchannel

# VHost server config
if [ ! -e $NXCONFDIR/helpchannel ]; then
    ln -sfT $CONFDIR/nginx.conf \
        $NXCONFDIR/helpchannel.conf
fi

# SSL self-signed key generation
if [ ! -f $CONFDIR/ssl.key -o ! -f $CONFDIR/ssl.pem ]
then
    echo "Auto-generate SSL self-signed certificate."
    openssl genrsa -out $CONFDIR/ssl.key 1024 2> /dev/null
    openssl req -new -subj /CN=$(hostname)/ -batch \
        -key $CONFDIR/ssl.key -out $CONFDIR/ssl.csr
    openssl x509 -req -days 3650 -in $CONFDIR/ssl.csr \
        -signkey $CONFDIR/ssl.key -out $CONFDIR/ssl.pem 2> /dev/null
    chown root:root $CONFDIR/ssl.key $CONFDIR/ssl.pem
    chmod 600       $CONFDIR/ssl.key $CONFDIR/ssl.pem
fi

ln -s /usr/share/gecos/helpchannel/repeater/ultravnc_repeater.pl /usr/bin/ultravnc_repeater

chkconfig nginx on
chkconfig gecoshc_repeater on
chkconfig gecoshc_ws_client on
chkconfig gecoshc_ws_server on

if [ -f /usr/bin/firewall-cmd ]
then
  # Open HTTPS port
  firewall-cmd --permanent --add-service=https
  systemctl restart firewalld
fi



%postun -n gecos-help-channel-server
if [ "$1" = "0" ]; then
    NXCONFDIR=/etc/nginx/conf.d/
    rm -f $NXCONFDIR/helpchannel.conf
    service nginx restart
	rm -f /usr/bin/ultravnc_repeater
fi

%clean -n gecos-help-channel-server
rm -rf $RPM_BUILD_ROOT

%files -n gecos-help-channel-server
%defattr(-,root,root)
/etc/init.d/gecoshc_repeater
/etc/init.d/gecoshc_ws_client
/etc/init.d/gecoshc_ws_server
/etc/gecos/*
/usr/share/gecos/*
/usr/lib/systemd/system/*.service
%defattr(0755,root,root)
%config /usr/share/gecos/helpchannel/repeater/ultravnc_repeater.pl
%dir /var/log/gecos

%changelog -n gecos-help-channel-server


