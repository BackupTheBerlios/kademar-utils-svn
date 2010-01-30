#
# Regular cron jobs for the kademar-khronos package
#
0 4	* * *	root	[ -x /usr/bin/kademar-khronos_maintenance ] && /usr/bin/kademar-khronos_maintenance
