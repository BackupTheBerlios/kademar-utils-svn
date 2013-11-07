#!/usr/bin/env python

from distutils.core import setup
import glob

images = glob.glob('src/img/*.png')
scripts = glob.glob('src/scripts/*')
daemon = glob.glob('src/daemon/cadidaemon')
tr = glob.glob('src/caditray/tr/*.qm')
dfiles = ['LICENSE','README','ChangeLog','AUTHORS','TODO']

setup(name='cadi',
      version='0.1',
      license='GPL2',
      description='The CADI systray for everithing',
      author=['Adonay Sanz'],
      author_email=['adonay@kademar.org'],
      url='http://www.kademar.org',
      package_dir={'caditray':'src/caditray'},
      packages=['caditray'],
      data_files=[ ('share/caditray/', dfiles),
                  ('share/applications' , ['caditray.desktop']),
                  ('/usr/share/polkit-1/actions' , ['src/daemon/org.archlinux.pkexec.cadidaemon.policy']),
                  ('/etc/polkit-1/localauthority/50-local.d' , ['src/daemon/cadi-admin-group.pkla']),
                  ('/etc/polkit-1/rules.d' , ['src/daemon/99-cadi-admin-group.rules']),
                  ('/etc/dbus-1/system.d/' , ['src/daemon/org.freedesktop.CADI.conf']),
                  ('share/autostart'    , ['caditray.desktop']),
                  ('share/caditray/'    , ['src/caditray/caditray.ui']),
                  ('share/caditray/img' , images),
                  #('share/caditray/scripts' , scripts),
                  ('lib/cadi/' , daemon),
                  ('share/caditray/tr'  , tr),
                  ],
                  #
      scripts=['src/bin/caditray']
)

