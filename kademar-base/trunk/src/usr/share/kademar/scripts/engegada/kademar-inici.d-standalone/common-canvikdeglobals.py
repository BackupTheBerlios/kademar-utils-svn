#!/usr/bin/python

#
# DEPRECATED A FAVOR DE KDE-KDEGLOBALS (bash)
#

#Ja no es fa res amb la paperera pq ho gestiona el propi KDE 3.4

# /home/kademar/.kde3/share/config/kdeglobals canviar dins seccio [Paths] el autostart, desktop i trash per catala o castella

import os
import sys

dirbase='/usr/share/kademar/scripts'
sys.path.insert(0, dirbase)

from funcions_k import *

if len(sys.argv)>1:
    usuari=sys.argv[1]
else:
    usuari='kademar'

if usuari=="skel":
    home="/etc/skel/"
else:
    home="/home/"+usuari+"/"

fitxer=home+'.kde3/share/config/kdeglobals'

casa=home
noms=[['Escriptori','Autoengega','Paperera'],
           ['Escritorio','Autoarranque','Papelera'],
           ['Desktop','Autostart','Trash']]

numllengua=idioma()   # crida a la funcio que detecta el idioma que esta instalat per defecte

#primer llegim el fitxer kdeglobals en la totalitat i ho assignem a la variable llista
f=open(fitxer,'r')
llista=f.readlines()
f.close()
linea=0
# fitxer='/home/kademar/kdeglobals'   # per fer proves, descomentar aquesta linea aixi no es sobreescriu el original

#despres contem les linies fins a trobar [Paths]
f=open(fitxer,'w')
for x in llista:
    if x[:7]<>'[Paths]':
        f.write(x)
        linea+=1
    else:
        break
    
# i ara mirem, a partir de la linia seguent a Paths, si hi ha linia Desktop, Autostart i Trash 
#i ho substituim per la que toqui en el idioma instalat    
for i in range(linea,len(llista)):
    if llista[i][:7]=='Desktop':
        desktop0=llista[i][14:-1]
        desktop1=noms[numllengua][0]
        f.write('Desktop=$HOME/'+noms[numllengua][0]+'\n')
    elif llista[i][:9]=='Autostart':
        autostart0=llista[i][16:-1]
        autostart1='.kde3/'+noms[numllengua][1]
        f.write('Autostart=$HOME/.kde3/'+noms[numllengua][1]+'\n')
#     elif llista[i][:5]=='Trash':
#         trash0=llista[i][12:-1]
#         trash1=noms[numllengua][0]+'/'+noms[numllengua][2]
#         f.write('Trash=$HOME/'+noms[numllengua][0]+'/'+noms[numllengua][2]+'\n')
    else:
        f.write(llista[i])
            
f.close()
# ara renombrem els directoris anteriors als noms actualitzats al idioma
# os.system('mv '+casa+trash0+'  '+casa+'temporal') # primer renombrem el trash perque es troba dins del desktop
os.system('mv '+casa+desktop0+'  '+casa+desktop1) # renombrem el desktop
os.system('mv '+casa+autostart0+'  '+casa+autostart1) # renombrem el autostart
#os.system('ln -s '+casa+desktop1+' '+casa+'Desktop 2>/dev/null') # Fem un link a $HOME/Desktop, per mantenir els Standards
# os.system('mv '+casa+'temporal'+'  '+casa+trash1) # renombrem al nom final el trash, dins del nou desktop
    
