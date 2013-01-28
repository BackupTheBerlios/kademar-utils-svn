[[ -z $DISPLAY && $XDG_VTNR -eq 7 ]] && /usr/bin/desktop-selector-daemon >> $HOME/.xsession-errors 2>&1
