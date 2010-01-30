#
# Regular cron jobs for the audioconversor package
#
0 4	* * *	root	[ -x /usr/bin/audioconversor_maintenance ] && /usr/bin/audioconversor_maintenance
