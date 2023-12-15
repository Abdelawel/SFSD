from pickle import dumps, loads
from sys import getsizeof
global b #Nombre maximal d'enregistrement dans le buffer ou le bloc
global tnom #La taille du champ Nom
global tprénom #La taille du champ Prénom
global tmat #La taille du champ Matricule
global tniveau #La taille du champ Niveau
global tsupprimer #La taille du champ indiquant l'effacement logique de l'enregistrement
global bufsize #La taille dubfuffer ou du bloc
b = 3
tmat = 20 ## size of the champs
tnom = 20
tprenom = 20
tniveau = 10
tsupprimer = 1
etud1 = '#' * (tmat + tnom + tprenom + tniveau + tsupprimer)
buf = [0, [etud1] * b] #Utilisé pour le calcul de la taille du buffer
bufsize = getsizeof(dumps(buf)) + (len(etud1) + 1) *  (b - 1) #Formule de calcul de la taille du buffer
#print(bufsize)

####################################################################
####################################################################

def resize_chaine(chaine, maxtaille):
    """Fonction de redémentionnement des champs de l'enregistrement afin de ne pas avoir des problèmes de taille"""
    for i in range(len(chaine),maxtaille):
          chaine = chaine + '#' 
    return chaine

####################################################################
####################################################################

def Creer_fichier():
    """ Procédure de création d'un fichier binaire"""
    fn = input("Donner le nom du fichier : ")
    j = 0 #Parcours des enregistrement
    i = 0 #Parcours des blocs
    n = 0 #Nombre des enregistrements
    #initialisation du buffer : 
    buf_tab = [etud1]*b
    buf_nb = 0 #buf_nb représente le nombre d'enregistrements dans le bloc
    try:
        f = open(fn, "wb")
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
        Etud = Matricule + Nom + Prenom + Niveau + '0' #'0' pour non-supprimé
        n += 1 #Augmenter le nombre d'enregistrement
        if(j < b): #bloc non-plain
            buf_tab[j] = Etud
            buf_nb += 1 #Augmenter le nombre d'enregistrement
            j += 1
        else: #bloc plain
            buf=[buf_nb, buf_tab]
            ecrireBloc(f, i, buf) #Ecrire le bloc dans le fichier
            buf_tab=[etud1] * b #Créer un nouveau bloc
            #Mettre dans le bloc le nouveau enregistrement
            buf_nb = 1 
            buf_tab[0] = Etud
            j = 1
            i += 1 #Augmenter le nombre de blocs
        rep = input("Un autre étudiant à ajouter O/N ? ")
    buf=[j,buf_tab]
    ecrireBloc(f, i, buf) #Ecrire le dernier bloc
    affecter_entete(f, 0, n) #Ecrire la première caractéristique
    affecter_entete(f, 1, i+1) #Ecrire la deuxième caractéristique
    f.close()

####################################################################
####################################################################

def affecter_entete(f, offset, val):
    """Fonction pour écrire les caractéristiques dans le fichier selon 'offset'"""
    Adr = offset * getsizeof(dumps(0))
    f.seek(Adr, 0)
    f.write(dumps(val))
    return

####################################################################
####################################################################

def ecrireBloc(f, ind, buff):
    """Procédure pour écrire le bloc dans le fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    f.write(dumps(buff))
    return

####################################################################
####################################################################

def lirebloc(f, ind) :
    """Fonction pour lire le bloc du fichier selon 'ind'"""
    Adr = 2 * getsizeof(dumps(0)) + ind * bufsize
    f.seek(Adr, 0)
    buf = f.read(bufsize)
    return (loads(buf))

####################################################################
####################################################################

def entete(f, ind):
    """fonction de récupération des caractéristiques selon 'ind'"""
    Adr = ind * getsizeof(dumps(0))
    f.seek(Adr, 0)
    tete = f.read(getsizeof(dumps(0)))
    return loads(tete)

####################################################################
####################################################################

def afficher_fichier():
    """Procédure d'affichage du fichier"""
    fn = input('Entrer le nom du fichier à afficher: ')
    f = open(fn,'rb')
    secondcar = entete(f,1) #Récupération de nombre des blocs
    print(f'votre fichier contient {secondcar} block \n')
    for i in range (secondcar):
        buf = lirebloc(f,i)
        buf_nb = buf[0]       
        buf_tab = buf[1]
        print(f'Le contenu du block {i+1} est:\n' )
        for j in range(buf_nb):
            if (buf_tab[j][-1] != '1'): #Ne pas affichier les enregistrements supprimés logiquement
                print(afficher_enreg(buf_tab[j]))
        print('\n')        
    f.close()
    return

####################################################################
####################################################################

def afficher_enreg(e):
    """Fonction de mise en forme des enregistrements
    Retourne une chaine de caractères sans le '#'"""
    Matricule = e[0:tmat].replace('#',' ')
    Nom = e[tmat:tnom+tmat].replace('#',' ')
    Prenom = e[tmat+tnom:tmat+tnom+tprenom].replace('#',' ')
    Niveau = e[tmat+tnom+tprenom:len(e) - 1].replace('#',' ')
    Supprimer = e[-1]
    return Matricule + ' ' + Nom + ' ' + Prenom + ' ' + Niveau + Supprimer

####################################################################
####################################################################

def search(file, key):
    T=False
    j=0
    i=0
    f=open(file, 'rb')
    while i<entete(f,1) and not T:
        buf=lirebloc(f,i)
        bufTab=buf[1]
        bufNb=buf[0]
        #print(bufNb)
        j=0
        while j<bufNb and not T :
            if bufTab[j][:tmat].rstrip('#')==key:
                T=True
                return[T,i,j]
            j+=1
        i+=1
    f.close()
    return [T,-1,-1]

####################################################################
####################################################################

def insert (file):
    Nom = input('Donner le nom : \n')
    Prenom = input('Donner le prenom : \n')
    Matricule = input('Donner le matricule : \n')
    Niveau = input('Donner le niveau : \n')
    Matricule = resize_chaine(Matricule, tmat)
    Nom = resize_chaine(Nom, tnom)
    Prenom = resize_chaine(Prenom, tprenom)
    Niveau = resize_chaine(Niveau, tniveau)
    #Enregistrement sous-forme d'une chaine de caractères
    Etud = Matricule + Nom + Prenom + Niveau + '0' #'0' pour non-supprimé
    f=open(file, 'rb+')
    i=entete(f,1)
    buf=lirebloc(f,i-1)
    bufNb=buf[0]
    bufTab=buf[1]
    #i=0
    j=0
    T=True
    if (bufNb<b) :
        bufTab[bufNb]=Etud
        bufNb+=1
        buf=[bufNb,bufTab]
        ecrireBloc(f,i-1,buf)
    else:
        buf=[0,[etud1]*b]
        bufNb=buf[0]
        bufTab=buf[1]
        bufTab[0]=Etud
        bufNb=1
        buf=[bufNb,bufTab]    
        ecrireBloc(f,i,buf)
        affecter_entete(f,1,entete(f,1)+1)
    affecter_entete(f,0,entete(f,0)+1)
    # while i<entete(f,1) and T :
    #     buf=lirebloc(f,i)
    #     bufNb=buf[0]
    #     bufTab=buf[1]
    #     j=0
    #     while j<b and T:
    #         if (bufTab[j][:tmat].replace('#','')==''):
    #             bufNb+=1
    #             bufTab[j]=Etud
    #             buf=[bufNb,bufTab]
    #             ecrireBloc(f,i-1,buf)
    #             affecter_entete(f,0,entete(f,0)+1)
    #             T=False
    #         j+=1
    #     i+=1
    # if (T):
    #     buf=[0, [etud1]*b]
    #     bufTab[0]=Etud
    #     bufNb=1
    #     buf=[bufNb,bufTab]    
    #     ecrireBloc(f,i,buf)
    #     affecter_entete(f,1,entete(f,1)+1)
    #     affecter_entete(f,0,entete(f,0)+1)
    f.close()

####################################################################
####################################################################

def deleteLogic (file):
    key=input("enter student's serial number:")
    f=open(file,'rb+')
    r=search(file,key)
    if(r[0]==True):
        buf=lirebloc(f,r[1])
        bufNb=buf[0]
        bufTab=buf[1]
        tmp= list(bufTab[r[2]])
        tmp[-1]='1'
        bufTab[r[2]]=''.join(tmp)
        #bufNb-=1 #if we keep it we will lose the element ...else it just shows that it's deleted
        buf=[bufNb, bufTab]
        ecrireBloc(f,r[1],buf) 
    else:
        print("this file already doesn't exist")    
    f.close()

####################################################################
####################################################################

def deletephisiq (file):
    key=input("enter student's serial number:")
    f=open(file,'rb+')
    r=search(file,key)
    if(r[0]==True):
        if(r[1]==entete(f,1)-1):
            buf=lirebloc(f,r[1])
            bufNb=buf[0]
            bufTab=buf[1]
            bufTab[r[2]]=bufTab[bufNb-1]
            bufNb-=1
            buf=[bufNb,bufTab]
            ecrireBloc(f,r[1], buf)
            if(bufNb==0):
                affecter_entete(f,1,entete(f,1)-1)
        else:
            buf1=lirebloc(f,entete(f,1)-1)
            buf1Nb=buf1[0]
            buf1Tab=buf1[1]
            buf=lirebloc(f,r[1])
            bufNb=buf[0]
            bufTab=buf[1]
            bufTab[r[2]]=buf1Tab[buf1Nb-1]
            buf1Nb-=1
            buf=[bufNb,bufTab]
            buf1=[buf1Nb,buf1Tab]
            ecrireBloc(f,r[1], buf)
            ecrireBloc(f,entete(f,1)-1, buf1)
            if(buf1Nb==0):
                affecter_entete(f,1,entete(f,1)-1)
        affecter_entete(f,0,entete(f,0)-1)
    else:
        print("this file already doesn't exist")
    f.close()
    
####################################################################
####################################################################

def fragmentation(file0, file1, file2):
    i=0
    i1=0
    i2=0
    j=0
    j1=0
    j2=0
    n1=0
    n2=0
    f=open(file0, 'rb')
    f1=open(file1, 'wb')
    f2=open(file2, 'wb')
    buf1=[0,[etud1]*b]
    buf1Tab=buf1[1]
    buf1Nb=buf1[0]
    buf2=[0,[etud1]*b]
    buf2Tab=buf2[1]
    buf2Nb=buf2[0]
    for i in range (entete(f,1)):
        buf=lirebloc(f,i)
        bufTab=buf[1]
        bufNb=buf[0]
        for j in range(bufNb):
            if(int(bufTab[j][:tmat].rstrip('#')) <=100000):
                n1+=1
                if(j1<b):
                    buf1Tab[j1]=bufTab[j]
                    j1+=1
                    buf1Nb+=1
                else:
                    buf1=[buf1Nb, buf1Tab]
                    ecrireBloc(f,i1,buf1)
                    # buf1=[0,[etud1]*b]
                    # buf1Tab=buf1[1]
                    # buf1Nb=buf1[0]
                    buf1Tab[0]=bufTab[j]
                    buf1Nb=1
                    j1=1
                    i1+=1
            else:
                n2+=1
                if(j2<b):
                    buf2Tab[j2]=bufTab[j]
                    j2+=1
                    buf2Nb+=1
                else:
                    buf2=[buf2Nb, buf2Tab]
                    ecrireBloc(f,i2,buf2)
                    # buf2=[0,[etud1]*b]
                    # buf2Tab=buf2[1]
                    # buf2Nb=buf2[0]
                    buf2Tab[0]=bufTab[j]
                    buf2Nb=1
                    j2=1
                    i2+=1
    buf1=[buf1Nb, buf1Tab]
    ecrireBloc(f,i1,buf1)
    buf2=[buf2Nb, buf2Tab]
    ecrireBloc(f,i2,buf2)
    affecter_entete(f1,1,i1+1)
    affecter_entete(f2,1,i2+1)
    affecter_entete(f1,0,n1)
    affecter_entete(f2,0,n2)
    f.close()
    f1.close()
    f2.close()
    
                
                    
        
    


#Creer_fichier()            
afficher_fichier()

# o=input('enter file name:')
# Key=input("who u r lookin for:")

# r=search(o, Key)
# if (r[0]==True):
#     print("exist")
#     print(f'dans le bloc :{r[1]+1} and position :{r[2]+1}')
# else:
#     print("exist not")
#     print(r[1],r[2])
# insert(o)
# # f=open('testins', 'rb+')
# # buf=lirebloc(f,2)
# # print(buf[0])
# #insert('2obj')
# afficher_fichier()
# deleteLogic(o)
# afficher_fichier()
# deletephisiq(o)
# afficher_fichier()

# fragmentation("txt","file1","file2")
# afficher_fichier()
# afficher_fichier()