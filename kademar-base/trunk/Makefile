
.PHONY: all install 

DESTDIR ?= /usr/local
all:  

	echo ""

install:
	cp -a src/* $(DESTDIR)
	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	
	#Copia del Instalador-dialog
	cp -a ../../instalador-dialog $(DESTDIR)/usr/share/kademar/utils/


	#kademar Modified
	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`

	#chown -R root:root $(DESTDIR) 2>/dev/null
	#chmod -R go=rX $(DESTDIR) 2>/dev/null
	
	#################
	#  kademar Zone #
	#################
	chmod -R 755 $(DESTDIR)/usr/share/kademar/scripts
# 	chmod -R 755 $(DESTDIR)/etc/network/if-up.d/kademar-apt-get-update

	####################
	# END kademar Zone #
	####################

	#posem permís de execució als scrips
# 	install -m 755 $(DESTDIR)/usr/local/bin/*
# 	install -m 755 $(DESTDIR)/sbin/*
# 	install -m 0440 -o root -g root etc/sudoers $(DESTDIR)/etc
	chmod +x $(DESTDIR)/usr/local/bin/*
	chmod +x $(DESTDIR)/usr/share/initramfs-tools/hooks/*

clean:
	rm -f `find . -name "*~"`
