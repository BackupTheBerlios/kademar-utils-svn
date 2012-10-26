
.PHONY: all install 

DESTDIR ?= /usr/local
all:  

	echo ""

install:
	cp -a src/* $(DESTDIR)
	chmod +x $(DESTDIR)/usr/bin/*
	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	#kademar Modified
	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`

	#chown -R root:root $(DESTDIR) 2>/dev/null
	#chmod -R go=rX $(DESTDIR) 2>/dev/null
	
clean:
	rm -f `find . -name "*~"`
