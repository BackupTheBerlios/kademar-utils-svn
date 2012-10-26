#
# Regular cron jobs for the kademar-extra-themes-ksplash package
#
0 4	* * *	root	[ -x /usr/bin/kademar-extra-themes-ksplash_maintenance ] && /usr/bin/kademar-extra-themes-ksplash_maintenance
