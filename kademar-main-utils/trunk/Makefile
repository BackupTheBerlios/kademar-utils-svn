
.PHONY: all install 

DESTDIR ?= /usr/local
all:  

	echo ""

install:
	cp -a src/* $(DESTDIR)
	#find $(DESTDIR) -name .svn -exec rm -r {} \;  || :
	#find src -type d -name '*.svn*' -prune -o -exec install -d  $(DESTDIR)/{} \;
	#find src -path '*.svn*' -prune -o (( -type d -o type l ) -exec install -m u+rw {}  $(DESTDIR)/{} \;)

	#################
	#  kademar Zone #
	#################
	mkdir -p $(DESTDIR)/usr/share/kademar/utils
	
	sh ../../instalador/prepare.sh 
	#Copia del Instalador
	cp -a ../../instalador $(DESTDIR)/usr/share/kademar/utils/
	#Prepara Instalador
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador/tr/*.ts
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador/*.project
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador/todo
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador/docs/*.odt

	#Initial installer prepare
	sh ../../instalador-nano/prepare.sh
	#Copia del Instalador-nano
	cp -a ../../instalador-nano $(DESTDIR)/usr/share/kademar/utils/
	#Prepara Instalador-nano
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador-nano/tr/*.ts
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador-nano/*.project
	rm -f $(DESTDIR)/usr/share/kademar/utils/instalador-nano/todo
	
	####################
	# END kademar Zone #
	####################
	
	#kademar Modified
	#Delete older backups from sourcecode executables
	cd $(DESTDIR) && rm -fr `find . -name ".svn"` && rm -fr `find . -name "*.pyc"` && rm -f `find . -name "*~"`

	#chown -R root:root $(DESTDIR) 2>/dev/null
	#chmod -R go=rX $(DESTDIR) 2>/dev/null
	chmod +x $(DESTDIR)/usr/local/bin/*

	#posem permís de execució als scrips
# 	install -m 755 $(DESTDIR)/usr/local/bin/*
# 	install -m 755 $(DESTDIR)/sbin/*
# 	install -m 0440 -o root -g root etc/sudoers $(DESTDIR)/etc

clean:
	rm -f `find . -name "*~"`
