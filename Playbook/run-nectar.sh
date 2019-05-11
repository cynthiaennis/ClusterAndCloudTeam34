#!/bin/bash

. ./unimelb-comp90024-group-40-openrc.sh; ansible-playbook --ask-become-pass nectar.yaml --key-file "./projectkey.pem" -vvv