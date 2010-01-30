#
# Regular cron jobs for the kademar-audacious-skins package
#
0 4	* * *	root	[ -x /usr/bin/kademar-audacious-skins_maintenance ] && /usr/bin/kademar-audacious-skins_maintenance
