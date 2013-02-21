#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
from PyQt4.QtSql import *

dbL = QSqlDatabase()
dbL = QSqlDatabase.addDatabase("QSQLITE")
dbL.setDatabaseName('rahisi.db')
dbL.open()

db_create='CREATE TABLE Programas (Codigo int(4) PRIMARY KEY, Categoria text, Nombre_en text, Nombre_es text, Nombre_ca text, Descripcion_en text, Descripcion_es TEXT, Descripcion_ca TEXT,  Ejecutable text, Icono TEXT, Categorias TEXT);'

dbL.exec_(db_create)
dbL.commit()

def gravaRegistre(registro):
    nombres=""
    for nom in registro:
        nombres=nombres+'"'+nom+'",'
    consulta='REPLACE INTO Programas values ('+nombres[:-1]+');'
    dbL.exec_(consulta)
    dbL.commit()
    #print numficheros, consulta

dir1="/usr/share/applications/"
dir2="/usr/share/applications/kde4/"
ficheros1=os.listdir(dir1)
if os.path.exists(dir2):
    ficheros2=os.listdir(dir2)
else:
    ficheros2=[]

#f=open("programes.txt",'w')
#f.write("Name | Name[es] | Name[ca] |GenericName[ca] | Exec | Categories\n\n")
#f.close()

def parse_fichero(fichero):
    f=open(fichero,'r')
    lineas=f.readlines()
    f.close()
    trobat_nombre_en=False
    trobat_nombre_es=False
    trobat_nombre_ca=False
    trobat_descripcion_en=False
    trobat_descripcion_es=False
    trobat_descripcion_ca=False
    trobat_ejecutable=False
    trobat_categoria=False
    trobat_icono=False
    nombre_en=""
    nombre_es=""
    nombre_ca=""
    descripcion_en=""
    descripcion_es=""
    descripcion_ca=""
    ejecutable=""
    categoria=""
    categorias=""
    icono=""
    #f=open("programes.txt",'a')

    for i in lineas:
        if i[:5]=="Icon=":
            icono=i[5:].strip()
            trobat_icono=True
        if i[:11]=="Categories=":
            categoria=i[11:].strip()
            categorias=categoria
            trobat_categoria=True
        if i[:5]=="Name=":
            nombre_en=i[5:].strip()
            trobat_nombre_en=True
        if i[:9]=="Name[es]=":
            nombre_es=i[9:].strip()
            trobat_nombre_es=True
        if i[:9]=="Name[ca]=":
            nombre_ca=i[9:].strip()
            trobat_nombre_ca=True
        if i[:12]=="GenericName=":
            descripcion_en=i[12:].strip()
            trobat_descripcion_en=True
        if i[:16]=="GenericName[es]=":
            descripcion_es=i[16:].strip()
            trobat_descripcion_es=True
        if i[:16]=="GenericName[ca]=":
            descripcion_ca=i[16:].strip()
            trobat_descripcion_ca=True
        if i[:5]=="Exec=":
            ejecutable=i[5:]
            if ejecutable.find('%')>=0:
                ejecutable=ejecutable[:ejecutable.find('%')]
            if ejecutable.find('"')>=0:
                ejecutable=ejecutable[:ejecutable.find('"')]
            if ejecutable.find('-caption')>=0:
                ejecutable=ejecutable[:ejecutable.find('-caption')]
            trobat_ejecutable=True

    if categoria=="":
        categoria="Varios"
    else:
        texto1=categoria.split(";")[0]
        if len(categoria.split(";"))>2:
            texto2=categoria.split(";")[1]
            texto3=categoria.split(";")[2]
        else:
            if len(categoria.split(";"))>1:
                texto2=categoria.split(";")[0]
                texto3=categoria.split(";")[1]
            else:
                texto2=texto1
                texto3=texto1

        if (texto1=="Qt" and texto2=="KDE") or (texto1=="KDE" and texto2=="Qt") or (texto1=="GNOME" and texto2=="GTK") or (texto1=="GTK" and texto2=="GNOME"):
            categoria=texto3
        else:
            if (texto1=="GTK") or (texto1=="Application"):
                categoria=texto2
            else:
                categoria=texto1

    if nombre_es=="":
        nombre_es=nombre_en
    if nombre_ca=="":
        nombre_ca=nombre_es
    if descripcion_en=="":
        descripcion_en=nombre_en
    if descripcion_es=="":
        descripcion_es=nombre_en
    if descripcion_ca=="":
        descripcion_ca=nombre_en
    Codigo=str(numficheros)
    Categoria=categoria
    Nombre_en=nombre_en
    Nombre_es=nombre_es
    Nombre_ca=nombre_ca
    Descripcion_en=descripcion_en
    Descripcion_es=descripcion_es
    Descripcion_ca=descripcion_ca
    Ejecutable=ejecutable
    Icono=icono
    Categorias=categorias
    registro=['8888','Rahisi','newRow','newRow','newRow','newRow','newRow','newRow','newRow','/usr/share/icons/hicolor/32x32/apps/kmenuedit.png','newRow']
    registro=[Codigo,Categoria,Nombre_en,Nombre_es,Nombre_ca,Descripcion_en,Descripcion_es,Descripcion_ca,Ejecutable,Icono,Categorias]
    gravaRegistre(registro)

    #f.write(categoria+"|"+nombre_en+"|"+nombre_ca+"|"+descripcion_ca+"|"+ejecutable+"|"+icono+"\n")
    #f.write("\n")
    #f.close()

numficheros=0

for i in ficheros1:
    fitxer=os.path.splitext(i)
    if fitxer[1]==".desktop":
        numficheros+=1
        parse_fichero(dir1+"/"+i)

for i in ficheros2:
    fitxer=os.path.splitext(i)
    if fitxer[1]==".desktop":
        numficheros+=1
        parse_fichero(dir2+"/"+i)
registro=['8888','Rahisi','newRow','newRow','newRow','newRow','newRow','newRow','newRow',' ',' ']
gravaRegistre(registro)
registro=['8889','Rahisi','Exit Pc','Apagar Pc','Tancar Pc','Shutdown Pc','Apaga el ordenador','Tanca el Pc','qdbus org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout 30 2 2','/usr/share/icons/hicolor/32x32/apps/kshutdown.png',' ']
gravaRegistre(registro)
    
dbL.close()


