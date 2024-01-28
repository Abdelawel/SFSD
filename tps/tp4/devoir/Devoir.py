from pickle import dumps, loads
from os.path import getsize
import os
from sys import getsizeof
global b #Nombre maximal d'enregistrement dans le buffer ou le bloc
global tnom #La taille du champ Nom
global tpre #La taille du champ pre
global tmat #La taille du champ Matricule
global tniveau #La taille du champ Niveau
global tefface #La taille du champ indiquant l'effacement logique de l'enregistrement
global taillebuf #La taille dubfuffer ou du bloc

fn0='fe.txt'
fn1='f1.txt'
fn2='f2.txt'
b=3
tmat = 20
tnom = 20
tprenom = 20
tniveau = 10
tefface = 1
max_index = 100
index=[0,(0,0)]
tindex=[0,[index]*max_index]
etud1 = '#' * (tmat + tnom + tprenom + tniveau + tefface)
buf = [0, -1, [etud1] * b] 
taillebuf = getsizeof(dumps(buf)) + (len(etud1) + 1) *  (b - 1) 
print(taillebuf)

def resize_chaine(chaine, maxtaille):
    """Fonction de redémentionnement des champs de l'enregistrement afin de ne pas avoir des problèmes de taille"""
    for i in range(len(chaine),maxtaille):
          chaine = chaine + '#' 
    return chaine



def affecter_entete(f, offset, val):
    """Fonction pour écrire les caractéristiques dans le fichier selon 'offset'"""
    Adr = offset * getsizeof(dumps(0))
    f.seek(Adr, 0)
    f.write(dumps(val))
    return



def ecrireBloc(f, ind, buff):
    """Procédure pour écrire le bloc dans le fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * taillebuf
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return



def lireBloc(f, ind) :
    """Fonction pour lire le bloc du fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * taillebuf
    f.seek(Adr, 0)
    buf = f.read(taillebuf)
    return (loads(buf))



def entete(f, ind):
    """Function to retrieve characteristics based on 'ind'"""
    Adr = ind * getsizeof(dumps(0))
    f.seek(Adr, 0)
    tete = f.read(getsizeof(dumps(0)))
    return loads(tete)



def creer_fichier():
    """ Procédure de création d'un fichier binaire"""
    j = 0 
    i = 0 
    n = 0 
    #initialisation du buffer : 
    buf_tab = [etud1]*b
    buf_nb = 0 
    try:
        f = open(fn0, "wb")
        f1 = open(fn2, "wb")
    except:
        print("Creation du fichier est impossible ")
    
    rep = 'O'
    while (rep.upper() == 'O'):
        #Lecture des information :
        Nom = input('Donner le nom : \n')
        Prenom = input('Donner le prenom : \n')
        Matricule = input('Donner le matricule : \n')
        Niveau = input('Donner le niveau : \n')
        #Redémentionnement des informations : 
        Matricule = resize_chaine(Matricule, tmat)
        Nom = resize_chaine(Nom, tnom)
        Prenom = resize_chaine(Prenom, tprenom)
        Niveau = resize_chaine(Niveau, tniveau)
        #Enregistrement sous-forme d'une chaine de caractères
        Etud = Matricule + Nom + Prenom + Niveau + '0' 
        n += 1 
        if(j < b): #bloc non-plain
            buf_tab[j] = Etud
            buf_nb += 1 
            j += 1
        else: #bloc plain
            buf=[buf_nb, -1 ,buf_tab]
            ecrireBloc(f, i, buf) 
            buf_tab=[etud1] * b 
            buf_nb = 1 
            buf_tab[0] = Etud
            j = 1
            i += 1 
        rep = input("Un autre étudiant à ajouter O/N ? ")
    buf=[j,-1,buf_tab]
    ecrireBloc(f, i, buf) 
    affecter_entete(f, 0, n) #Ecrire la première caractéristique
    affecter_entete(f, 1, i+1)
    f.close()


def afficher_fichier(fn1,fn2):
    f1 = open(fn1,'rb')
    f2=open(fn2,'rb')
    secondcar = entete(f1,1) #Récupération de nombre des blocs
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (0,secondcar):
        print("fichier f1 \n")
        buf = lireBloc(f1,i)
        buf_nb = buf[0]       
        buf_tab = buf[2]
        buf_suiv=buf[1]
        print(f'Le contenu du block {i+1} est:\n' )
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1'): 
                print(afficher_enreg(buf_tab[j]))
        print('\n') 
        if buf_suiv!=-1:
            print('fichier f2 \n')
        while buf_suiv != -1 :
            k=buf_suiv
            buf=lireBloc(f2,buf_suiv)
            buf_nb = buf[0]       
            buf_tab = buf[2]
            buf_suiv=buf[1]
            print(f'Le contenu du block {k} est:\n' )
            for j in range(buf_nb):
              if (buf_tab[j][-1] != '1'): #Ne pas affichier les enregistrements supprimés logiquement
               print(afficher_enreg(buf_tab[j]))
            print('\n') 
    f1.close()
    f2.close()
    return


def reorganiser_fichier(A):
    
    f1 = open(fn0, 'rb+')
    f2 = open(fn1, 'wb+')
    buf1 = [0, -1, [etud1] * b]
    secondcar = entete(f1, 1)
    firstcar = entete(f1, 0)
    n = 0
    p = '1'
    k = 0
    l = 0

    while n < firstcar:
        i=0
        j=0
        buf = lireBloc(f1, i)
        p=buf[2][j][-1]
        while i < secondcar and p == '1':
            buf = lireBloc(f1, i)
            while j<buf[0] and p=='1':
                p=buf[2][j][-1]
                j=j+1
            if p=='1':
                i=i+1
                j=0    
        bi = [buf[2][j],(i,j)]    

        for i in range(0, secondcar):
            buf = lireBloc(f1, i)
            buf_nb = buf[0]
            buf_tab = buf[2]
            r=0
            for j in range(0, buf_nb):
                if (bi[0][0:tmat].replace('#', '') > buf_tab[j][0:tmat].replace('#', '')   and buf_tab[j][-1] == '0'):
                    bi = [buf_tab[j], (i, j)]
        buf = lireBloc(f1, int(bi[1][0]))
        modified_string = buf[2][bi[1][1]][:-1] + '1'
        buf[2][bi[1][1]] = modified_string
        ecrireBloc(f1, bi[1][0], buf)

        if k < b:
            buf1[2][k] = bi[0]
            buf1[0] = buf1[0] + 1
            k = k + 1
        else:
            ecrireBloc(f2, l, buf1)
            affecter_entete(f2, 1, l)
            l = l + 1
            buf1=[0,-1,[etud1]*b]
            buf1[2][0] = bi[0]
            buf1[0] = 1
            k = 1
        n = n + 1
    ecrireBloc(f2, l, buf1)
    affecter_entete(f2, 1, l + 1)
    affecter_entete(f2, 0, n)
    fix_fich(f1)
    f1.close()
    f2.close()
    A=creer_tindex()
    return


def afficher_enreg(e):
    """Fonction de mise en forme des enregistrements
        Retourne une chaine de caractères sans le '#'"""
    Matricule = e[0:tmat].replace('#',' ')
    Nom = e[tmat:tnom+tmat].replace('#',' ')
    Prenom = e[tnom+tmat:tnom+tmat+tprenom].replace('#',' ')
    Niveau = e[tnom+tprenom+tmat:len(e) - 1].replace('#',' ')
    efface = e[-1]
    return Matricule + ' ' + Nom + ' ' + Prenom + ' ' + Niveau + efface

def afficher_tabindex(tindex):   
   for i in range(0,tindex[0]):
    print(tindex[1][i])
   return

def creer_tindex():

    f=open(fn1,'rb+')
    i=0
    secondcar=entete(f,1)
    print(entete(f,1))
    for i in range(0,secondcar):
        buf=lireBloc(f,i)
        buf_nb=buf[0]
        buf_tab=buf[2]
        tindex[0]=tindex[0]+1
        tindex[1][i]=[int(buf_tab[buf_nb-1][0:tmat].replace('#','')),(i,buf_nb-1)]
    f.close()    
    return tindex   
        

def fix_fich(f):
    secondcar = entete(f, 1)
    for i in range(0, secondcar):
        buf = lireBloc(f, i)
        for j in range(0, buf[0]):
            modified_string = buf[2][j][:-1] + '0'
            buf[2][j] = modified_string
        ecrireBloc(f, i, buf)
    f.close()

def requete_intervalle(A, B, tindex):
    k1=recherche(A,tindex)
    k2=recherche(B,tindex)
    f1=open(fn1,'rb')
    f2=open(fn2,'rb')
    if k1[0][0]>=entete(f1,1):
        k1[0][0]=k1[0][0]-1
    for i in range(k1[0][0],k2[0][0]):
        buf = lireBloc(f1,i)
        buf_nb = buf[0]       
        buf_tab = buf[2]
        buf_suiv=buf[1]
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1' and int(buf_tab[j][0:tmat].replace('#',''))<= B and int(buf_tab[j][0:tmat].replace('#',''))>=A ): 
                print(afficher_enreg(buf_tab[j]))
        print('\n') 
        if buf_suiv!=-1:
         while buf_suiv != -1 :
            k=buf_suiv
            buf=lireBloc(f2,buf_suiv)
            buf_nb = buf[0]       
            buf_tab = buf[2]
            buf_suiv=buf[1]
            for j in range(buf_nb):
               if (buf_tab[j][-1] != '1' and int(buf_tab[j][0:tmat].replace('#',''))<= B and int(buf_tab[j][0:tmat].replace('#',''))>=A ): 
                print(afficher_enreg(buf_tab[j]))
            print('\n') 

    return 

def recherche(clé,tindex):

    f1=open(fn1,'rb')  
    f2=open(fn2,'rb')  
    buf = [0, -1, [etud1] * b]
    debord=False
    bs=tindex[0]-1
    bi=0
    trouv=False

    while bs>=bi and trouv==False:
        i=(bs+bi)//2
        if int(tindex[1][i][0])==clé:
           trouv=True
        else:
            if int(tindex[1][i][0])<clé:
                bi=i+1
            else:
                bs=i-1  
    if trouv==False:
        i=bi    
    if trouv==True:
        buf=lireBloc(f1,i)
        if int(buf[2][buf[0]-1][0:tmat].replace('#',''))==clé:
            p=(i,-1,buf[0]-1)
            trouv=True
            debord=False
        else:
            p=(i,buf[1],0)
            trouv=True
            debord=True
    else:
        pos=tindex[1][i][1]
        if i>tindex[0]-1:
            pos=tindex[1][tindex[0]-1][1]
        buf=lireBloc(f1,pos[0])
        buf_nb=buf[0]
        buf_tab=buf[2]
        buf_suiv=buf[1]
        stop=False
        trouv=False
        j=0
        while stop==False and trouv==False and j != buf_nb: 
            if int(buf_tab[j][0:tmat].replace('#',''))==clé:
                trouv=True
                stop=True
                debord=False
                p=(pos[0],-1,j)
            else:
                if int(buf_tab[j][0:tmat].replace('#',''))<clé:
                    j=j+1
                else:
                    stop=True
                    debord=False
                    p=(pos[0],-1,j)
        if stop==False :
            if buf_nb < b:
                p=(pos[0],-1,buf_nb)
                debord=False
            else:
                 debord=True
                 p=(pos[0],-1,0)
                 j=0
                 while buf_suiv!=-1 and stop==False and trouv==False:
                    k=buf_suiv
                    buf=lireBloc(f2,buf_suiv)
                    buf_nb=buf[0]
                    buf_suiv=buf[1]
                    buf_tab=buf[2]
                 while j!=buf_nb and stop==False and trouv==False:
                    if int(buf_tab[j][0:tmat].replace('#',''))==clé:
                        trouv=True
                        p=(pos[0],k,j)
                    j=j+1  
                 if trouv==False:
                     debord=False
                     p=(pos[0]+1,-1,0)
    f1.close() 
    f2.close()                    
    return (p,trouv,debord)     



def insertion(tindex):
    print('inserez un nouveau etudiant \n')
    Nom = input('Donner le nom : \n')
    Prenom = input('Donner le prenom : \n')
    Matricule = input('Donner le matricule : \n')
    Niveau = input('Donner le niveau : \n')
    Matricule = resize_chaine(Matricule, tmat)
    Nom = resize_chaine(Nom, tnom)
    Prenom = resize_chaine(Prenom, tprenom)
    Niveau = resize_chaine(Niveau, tniveau)
    Etud = Matricule + Nom + Prenom + Niveau + '0' 

    A=recherche(int(Etud[0:tmat].replace('#','')),tindex)
    f_1=open(fn1,'rb+')
    f_2=open(fn2,'rb+')
    buf1=buf
    buf2=buf
    if A[1]==False:
     if A[2]==True:
         buf1=lireBloc(f_1,A[0][0])
         if buf1[1]==-1:
             buf1[1]=entete(f_2,1)
             ecrireBloc(f_1,A[0][0],buf1)
             buf2[2][buf2[0]]=Etud
             buf2[0]=buf2[0]+1
             ecrireBloc(f_2,entete(f_2,1),buf2)
             affecter_entete(f_2,1,entete(f_2,1)+1)
         else:
             buf2=lireBloc(f_2,A[0][1])
             if buf2[0]<b:
                 buf2[2][buf[0]]=Etud
                 buf[0]=buf[0]+1
                 ecrireBloc(f_2,A[0][1],buf2)
             else:
                 buf2[1]=entete(f_2,1)
                 buf2=buf
                 buf2[2][buf[0]]=Etud
                 buf[0]=buf[0]+1
                 ecrireBloc(f_2,entete(f_2,1),buf2)
                 affecter_entete(f_2,1,entete(f_2,1)+1)
     else:
         if A[0][0]<entete(f_1,1):   
             buf1=lireBloc(f_1,A[0][0])
             print(entete(f_1,1))
         else:
             buf1=[0,-1,[etud1]*b]
             tindex[0]=tindex[0]+1
             affecter_entete(f_1,1,entete(f_1,1)+1) 
         if buf1[0]<b:
             for k in range (buf1[0]-1,A[0][2]-1,-1):
                 buf1[2][k+1]=buf1[2][k]
             buf1[2][A[0][2]]=Etud
             if A[0][2]==buf1[0]:
                 tindex[1][A[0][0]]=(int(Etud[0:tmat].replace('#','')),(A[0][0],A[0][2]))
             else:
                 tindex[1][A[0][0]][1]=(A[0][0],buf1[0])
             buf1[0]=buf1[0]+1
             ecrireBloc(f_1,A[0][0],buf1)
         else:
             x=buf1[2][buf1[0]-1]
             for k in range(buf1[0]-1,A[0][2]-1,-1):
                 buf1[2][k]=buf1[2][k-1]
             buf1[2][A[0][2]]=Etud 
             if buf1[1]==-1:
                 if os.path.getsize(fn2) == 0:
                  buf1[1]=0
                 else:
                  buf1[1]=entete(f_2,1)
                 buf2=buf
                 buf2[2][buf2[0]]=x
                 buf2[0]=buf2[0]+1
                 ecrireBloc(f_1,A[0][0],buf1)
                 ecrireBloc(f_2,buf1[1],buf2)
                 affecter_entete(f_2,1,buf1[1]+1)
             else:
                 i=buf1[1]
                 buf2=lireBloc(f_2,buf1[1])
                 while buf2[1]!=-1:
                     i=buf2[0]
                     buf2=lireBloc(f_2,buf2[1])
                 if buf2[0]<b:
                     buf2[2][buf2[0]]=x
                     buf2[0]=buf2[0]+1
                     ecrireBloc(f_2,i,buf2)
                 else:
                     buf2[1]=entete(f_2,1)
                     ecrireBloc(f_2,i,buf2)
                     buf2=buf
                     buf2[2][buf2[0]]=x
                     buf2[0]=buf2[0]+1
                     ecrireBloc(f_2,entete(f_2,1),buf2)
                     affecter_entete(f_2,1,entete(f_2,1)+1)
                 ecrireBloc(f_1,A[0][0],buf1)
    f_1.close()
    f_2.close()       
    return


def suppression(clé,tindex):
    A=recherche(clé,tindex)
    if A[1]==True:
        if A[2]==False:
            f=open(fn1,'rb+')
            buf=lireBloc(f,A[0][0])
            original_string = buf[2][A[0][2]]
            modified_string = original_string[:-1] + '1'
            buf[2][A[0][2]] = modified_string
            ecrireBloc(f,A[0][0],buf)
        else: 
            f=open(fn2,'rb+')
            buf=lireBloc(f,A[0][1])
            boriginal_string = buf[2][A[0][2]]
            modified_string = original_string[:-1] + '1'
            buf[2][A[0][2]] = modified_string
            ecrireBloc(f,A[0][0],buf)


creer_fichier()
reorganiser_fichier(tindex)
afficher_fichier(fn0,fn2)
afficher_fichier(fn1,fn2)
afficher_tabindex(tindex)
insertion(tindex)
afficher_fichier(fn1,fn2)
afficher_tabindex(tindex)
print(recherche(15,tindex))
suppression(15,tindex)
afficher_fichier(fn1,fn2)
requete_intervalle(10,20, tindex)