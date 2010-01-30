#
# Regular cron jobs for the kademar-lyra package
#
0 4	* * *	root	[ -x /usr/bin/kademar-lyra_maintenance ] && /usr/bin/kademar-lyra_maintenance
