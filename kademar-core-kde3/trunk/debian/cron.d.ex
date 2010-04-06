#
# Regular cron jobs for the kademar-core-kde3 package
#
0 4	* * *	root	[ -x /usr/bin/kademar-core-kde3_maintenance ] && /usr/bin/kademar-core-kde3_maintenance
