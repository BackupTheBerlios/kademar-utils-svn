
.PHONY: all install 

DESTDIR ?= /usr/local
all:  

	echo ""

install:

	cp -a src/* $(DESTDIR)
	mkdir -p $(DESTDIR)/usr/share/kademar/utils
	
	#Initial cadi prepare
	sh ../../cadi/prepare.sh 
	#Copia del cadi
	cp -a ../../cadi $(DESTDIR)/usr/share/kademar/utils/
	cp -a ../../cadi/scripts $(DESTDIR)/usr/bin

	#Prepara cadi
	rm -f $(DESTDIR)/usr/share/kademar/utils/cadi/tr/*.ts
	rm -f $(DESTDIR)/usr/share/kademar/utils/cadi/*.project	

	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	#posem permís de execució als scrips
# 	install -m 755 $(DESTDIR)/usr/local/bin/*
# 	install -m 755 $(DESTDIR)/sbin/*
# 	install -m 0440 -o root -g root etc/sudoers $(DESTDIR)/etc

	chmod -x $(DESTDIR)/usr/share/menu/cadi

	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`


clean:
	rm -f `find . -name "*~"`
