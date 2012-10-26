#!/bin/bash

[ -e /mnt/live/data ] && 	touch "/mnt/live/$(hal-get-property --udi  $(sh /usr/share/kdemar/utils/kdemarcenter/scripts/grephalinfo.sh  /dev/`cat /mnt/live/data` parent ) --key storage.bus)"