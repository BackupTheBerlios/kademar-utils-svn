
.PHONY: all install 

DESTDIR ?= /usr/local
all:  

	echo ""

install:

	cp -a src/* $(DESTDIR)
	mkdir -p $(DESTDIR)/usr/share/kademar/utils
	
	#Initial installer kademarcenter
	sh ../../kademarcenter/prepare.sh 
	#Copia de kademarcenter
	cp -a ../../kademarcenter $(DESTDIR)/usr/share/kademar/utils/kademarcenter
	#Prepara kademarcenter
	rm -f $(DESTDIR)/usr/share/kademar/utils/kademarcenter/tr/*.ts
	rm -f $(DESTDIR)/usr/share/kademar/utils/kademarcenter/*.project

	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	#posem permís de execució als scrips
# 	install -m 755 $(DESTDIR)/usr/local/bin/*
# 	install -m 755 $(DESTDIR)/sbin/*
# 	install -m 0440 -o root -g root etc/sudoers $(DESTDIR)/etc

	chmod -R 755 $(DESTDIR)/usr/share/kademar/utils/kademarcenter/scripts
	chmod 755 $(DESTDIR)/usr/bin/*

	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`


clean:
	rm -f `find . -name "*~"`
