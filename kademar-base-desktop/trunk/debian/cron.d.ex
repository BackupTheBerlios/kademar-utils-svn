#
# Regular cron jobs for the kademar-base-desktop package
#
0 4	* * *	root	[ -x /usr/bin/kademar-base-desktop_maintenance ] && /usr/bin/kademar-base-desktop_maintenance
