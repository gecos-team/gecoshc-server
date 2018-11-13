#!/bin/bash

set -e

MAKEINSTALLED=`rpm -qa | grep make | wc -l`
if [ "$MAKEINSTALLED" -eq 0 ]
then
	echo "Make must be installed. Please execute: sudo yum install make"
	exit
fi

AUTOCONFINSTALLED=`rpm -qa | grep autoconf | wc -l`
if [ "$AUTOCONFINSTALLED" -eq 0 ]
then
	echo "Autoconf must be installed. Please execute: sudo yum install autoconf"
	exit
fi


LIBTOOLINSTALLED=`rpm -qa | grep libtool | wc -l`
if [ "$LIBTOOLINSTALLED" -eq 0 ]
then
	echo "libtool must be installed. Please execute: sudo yum install libtool"
	exit
fi


RPMBUILDINSTALLED=`rpm -qa | grep rpm-build | wc -l`
if [ "$RPMBUILDINSTALLED" -eq 0 ]
then
	echo "rpm-build must be installed. Please execute: sudo yum install rpm-build"
	exit
fi



chmod +x autogen
./autogen
make
make dist-gzip

THISDIR=`pwd`

cp SPECS/help-channel-server.spec  $HOME/rpmbuild/SPECS/help-channel-server.spec
cp help-channel-server-*.tar.gz $HOME/rpmbuild/SOURCES/.

cd $HOME/rpmbuild/SPECS
rpmbuild -ba help-channel-server.spec

echo "END ;)"
