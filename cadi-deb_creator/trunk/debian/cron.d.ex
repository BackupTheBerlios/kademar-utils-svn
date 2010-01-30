#
# Regular cron jobs for the cadi package
#
0 4	* * *	root	[ -x /usr/bin/cadi_maintenance ] && /usr/bin/cadi_maintenance
