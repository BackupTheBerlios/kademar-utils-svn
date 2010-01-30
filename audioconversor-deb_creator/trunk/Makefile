
.PHONY: all install 

DESTDIR ?= /usr/local
all:  

	echo ""

install:

	cp -a src/* $(DESTDIR)
	mkdir -p $(DESTDIR)/usr/share/kademar/utils


	#Initial audioconversor prepare
	sh ../../audioconversor/prepare.sh 
	#Copia del audioconversor
	#Copia de Conversor_audio
	cp -a ../../audioconversor $(DESTDIR)/usr/share/kademar/utils

	#Prepara cadi
	rm -f $(DESTDIR)/usr/share/kademar/utils/audioconversor/tr/*.ts
	rm -f $(DESTDIR)/usr/share/kademar/utils/audioconversor/*.project	

	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	#posem permís de execució als scrips
# 	install -m 755 $(DESTDIR)/usr/local/bin/*
# 	install -m 755 $(DESTDIR)/sbin/*
# 	install -m 0440 -o root -g root etc/sudoers $(DESTDIR)/etc

	chmod -x $(DESTDIR)/usr/share/menu/audioconversor

	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`


clean:
	rm -f `find . -name "*~"`
