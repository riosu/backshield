#!/bin/bash

if ! which python3 > /dev/null 2>&1; then
    # CentOS6
    if [[ -e /etc/redhat-release ]]; then
        yum install -y https://centos6.iuscommunity.org/ius-release.rpm
        yum install -y python35u python35u-libs python35u-devel python35u-pip
        ln -s /usr/bin/python3.5 /usr/bin/python3
    fi
fi

# Create simlink
ln -s "`pwd`/backshield.py" /usr/bin/backshield
