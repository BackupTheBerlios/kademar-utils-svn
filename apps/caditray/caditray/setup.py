#!/usr/bin/env python

from distutils.core import setup
import glob

images = glob.glob('src/img/*.png')
tr = glob.glob('src/caditray/tr/*.qm')
dfiles = ['LICENSE','README','ChangeLog','AUTHORS','TODO']

setup(name='caditray',
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
                  ('share/caditray/'    , ['src/caditray/caditray.ui']),
                  ('share/caditray/img' , images),
                  ('share/caditray/tr' , tr),
                  ],
                  #
      scripts=['src/scripts/caditray']
)

