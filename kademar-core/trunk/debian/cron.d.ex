#
# Regular cron jobs for the kademar-core package
#
0 4	* * *	root	[ -x /usr/bin/kademar-core_maintenance ] && /usr/bin/kademar-core_maintenance
