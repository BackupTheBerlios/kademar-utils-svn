#
# Regular cron jobs for the kademar-core-kde4 package
#
0 4	* * *	root	[ -x /usr/bin/kademar-core-kde4_maintenance ] && /usr/bin/kademar-core-kde4_maintenance
