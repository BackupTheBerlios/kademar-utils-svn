#
# Regular cron jobs for the kademar-khronos-lite package
#
0 4	* * *	root	[ -x /usr/bin/kademar-khronos-lite_maintenance ] && /usr/bin/kademar-khronos-lite_maintenance
