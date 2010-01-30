#
# Regular cron jobs for the kademar-base package
#
0 4	* * *	root	[ -x /usr/bin/kademar-base_maintenance ] && /usr/bin/kademar-base_maintenance
