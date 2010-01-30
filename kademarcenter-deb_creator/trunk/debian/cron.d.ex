#
# Regular cron jobs for the kademarcenter package
#
0 4	* * *	root	[ -x /usr/bin/kademarcenter_maintenance ] && /usr/bin/kademarcenter_maintenance
