PYTHON=`which python`
PREFIX=/usr
DESTDIR=/
PKGNAME=caditray
VERSION=0.1.1

all: clean
# 	pyrcc4 -py3 -o src/caditray/resource.py src/caditray/resource.qrc

	# Update Translation
	lupdate-qt4 src/caditray/caditray.pro

	#Release translation
	lrelease-qt4 src/caditray/caditray.pro

	$(PYTHON) setup.py build

install: all
# 	pyrcc4 -py3 -o src/caditray/resource.py src/caditray/resource.qrc
	$(PYTHON) setup.py install --prefix $(PREFIX) --root $(DESTDIR)

clean:
	$(PYTHON) setup.py clean
	rm -rf build/

distclean: clean
	rm -rf dist/
	rm -rf pkg/
	rm -rf $(PKGNAME)-*.tar.gz

dist: distclean
	mkdir -p /tmp/pkg/$(PKGNAME)-$(VERSION)
	cp -Rf * /tmp/pkg/$(PKGNAME)-$(VERSION)
	mv /tmp/pkg .
	find . -name *.pyc | xargs rm -rf
	find . -name .svn | xargs rm -rf
	cd pkg/ && tar -cvzf ../$(PKGNAME)-$(VERSION).tar.gz $(PKGNAME)-$(VERSION)
	rm -rf pkg/
