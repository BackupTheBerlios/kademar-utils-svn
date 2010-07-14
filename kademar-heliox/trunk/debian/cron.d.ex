#
# Regular cron jobs for the kademar-heliox package
#
0 4	* * *	root	[ -x /usr/bin/kademar-heliox_maintenance ] && /usr/bin/kademar-heliox_maintenance
