#
# Regular cron jobs for the kademar-timidity-2.13.2 package
#
0 4	* * *	root	[ -x /usr/bin/kademar-timidity-2.13.2_maintenance ] && /usr/bin/kademar-timidity-2.13.2_maintenance
