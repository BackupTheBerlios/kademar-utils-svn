.PHONY: all install clean

DESTDIR ?= /usr/local
all:  

	echo ""

install:

	cp -a src/* $(DESTDIR)/
	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	#posem permís de execució als scrips
# 	chmod u+rwx $(DESTDIR)/usr/local/bin/*
# 	chmod +x $(DESTDIR)/usr/local/bin/*

	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`

	# CREA CONFIG 2ND STAGE
	#sh crea_config-2nd_stage
	

clean:
	rm -f `find . -name "*~"`
