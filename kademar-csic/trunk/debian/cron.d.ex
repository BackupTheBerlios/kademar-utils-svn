#
# Regular cron jobs for the kademar-csic package
#
0 4	* * *	root	[ -x /usr/bin/kademar-csic_maintenance ] && /usr/bin/kademar-csic_maintenance
