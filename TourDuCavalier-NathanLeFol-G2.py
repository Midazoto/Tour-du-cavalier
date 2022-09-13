# -*- coding: utf-8 -*-
"""
@author: NathanLeFol
"""
from tkinter import *
from tkinter import font

def voisin(pos,n): #Retourne la liste des voisins (Case accessible par le cavalier)
    lst=[] #Initialisation d'une liste pour stocké les résultats
    mouvx = [-2,-2,-1,-1,1,1,2,2] #Liste des déplacements possible sur l'axe x
    mouvy = [1,-1,2,-2,2,-2,1,-1] #Liste des déplacements possible sur l'axe y

    for i in range(0,8):#Recherche des 8 possibilitée
        x = pos[0] + mouvx[i] #X
        y = pos[1] + mouvy[i] #Y
        if x>=0 and y>=0 and x<n and y<n: #Vérification que x et y sont dans l'échiquier
            lst.append((x,y)) #Si oui alors on ajoute cette position à la liste
    return lst #Retourne la liste

def voisindispo(pos,echequier,parcouru): #Retourne la liste des voisin qui n'ont pas encore été parcouru
    dispo=[] #Initialisation d'une liste pour stocké les résultats
    for i in voisin(pos,len(echequier)): #Pour chaque voisin 
        if i not in parcouru: #Si le voisin n'a pas déjà été essayé
            if echequier[i[0]][i[1]]==0: #Si le voisin n'a pas déjà été parcouru dans le chemin
                dispo.append(i) #On ajoute le voisin à la liste
    return dispo #Retourne la liste

def tourNonEffectue(echequier,cycle,chemin,n): #Retourne True si il reste des cases à parcourir sur l'échiquier, False sinon
    NonEffectue=False #Initialistaion de la variable
    for i in echequier: #Pour chaque ligne de la matrice
        if 0 in i: #Si il y a un 0 sur la ligne alors
            NonEffectue=True #Le tour n'a pas été effectué
    if cycle and not NonEffectue: #Si le le cavalier à parcouru toute les cases et que l'utlisateur veux trouver un cycle
        if chemin[0] not in voisin(chemin[-1],n): #Si le point de départ ne fait pas partie des voisins du point d'arrivée alors 
            NonEffectue=True #On considère que l'algorythme n'a pas trouvé de solution
    return NonEffectue #Retournne la variable

def dessindamier(n,dessin,fen): #Dessine le damier
    dim = (n+1)*100
    dessin.grid(row = 1, column = 0, columnspan = 2, padx=5, pady=5)
    dessin.create_line(100, 100, dim, 100, fill= 'black', width=10)
    dessin.create_line(100, dim, dim, dim, fill= 'black', width=10)
    dessin.create_line(100, 100, 100, dim, fill= 'black', width=10)
    dessin.create_line(dim, 100, dim, dim, fill= 'black', width=10)
    for i in range(n):
        dessin.create_line((i+1)*100,100,(i+1)*100,dim,fill='black',width=5)
        dessin.create_line(100,(i+1)*100,dim,(i+1)*100,fill='black',width=5)
    fen.update_idletasks()
    fen.update()


def dessindeplacement(pos,newpos,fen,dessin,final=False,i=1,cycle = False): #Dessine un déplacement d'une case à une autre
    if i==0:
        dessin.create_oval((pos[0]+1)*100+50-20,(pos[1]+1)*100+50-20, (pos[0]+1)*100+50+20,(pos[1]+1)*100+50+20, fill='blue')
        dessin.create_line((pos[0]+1)*100+50,(pos[1]+1)*100+50,(newpos[0]+1)*100+50,(newpos[1]+1)*100+50,fill='black',width=3)
        dessin.create_oval((newpos[0]+1)*100+50-20,(newpos[1]+1)*100+50-20, (newpos[0]+1)*100+50+20,(newpos[1]+1)*100+50+20, fill='red')
    elif cycle:
        dessin.create_oval((pos[0]+1)*100+50-20,(pos[1]+1)*100+50-20, (pos[0]+1)*100+50+20,(pos[1]+1)*100+50+20, fill='yellow')
        dessin.create_line((pos[0]+1)*100+50,(pos[1]+1)*100+50,(newpos[0]+1)*100+50,(newpos[1]+1)*100+50,fill='red',width=3)
        dessin.create_oval((newpos[0]+1)*100+50-20,(newpos[1]+1)*100+50-20, (newpos[0]+1)*100+50+20,(newpos[1]+1)*100+50+20, fill='blue')

    else:
        if not final:
            dessin.create_oval((pos[0]+1)*100+50-20,(pos[1]+1)*100+50-20, (pos[0]+1)*100+50+20,(pos[1]+1)*100+50+20, fill='red')
            dessin.create_line((pos[0]+1)*100+50,(pos[1]+1)*100+50,(newpos[0]+1)*100+50,(newpos[1]+1)*100+50,fill='black',width=3)
            dessin.create_oval((newpos[0]+1)*100+50-20,(newpos[1]+1)*100+50-20, (newpos[0]+1)*100+50+20,(newpos[1]+1)*100+50+20, fill='red')
        else:
            dessin.create_oval((pos[0]+1)*100+50-20,(pos[1]+1)*100+50-20, (pos[0]+1)*100+50+20,(pos[1]+1)*100+50+20, fill='green')
            dessin.create_line((pos[0]+1)*100+50,(pos[1]+1)*100+50,(newpos[0]+1)*100+50,(newpos[1]+1)*100+50,fill='black',width=3)
            dessin.create_oval((newpos[0]+1)*100+50-20,(newpos[1]+1)*100+50-20, (newpos[0]+1)*100+50+20,(newpos[1]+1)*100+50+20, fill='yellow')
    fen.update_idletasks()
    fen.update()

def dessinUndoLent(pos,prevpos,fen,dessin,n): #Permet d'annuler la représentation d'un déplacement (Version Lente)
    dessin.create_oval((pos[0]+1)*100+50-20,(pos[1]+1)*100+50-20, (pos[0]+1)*100+50+20,(pos[1]+1)*100+50+20, fill='ivory',outline='ivory',tags="cercle")
    dessin.create_line((pos[0]+1)*100+50,(pos[1]+1)*100+50,(prevpos[0]+1)*100+50,(prevpos[1]+1)*100+50,fill='ivory',width=3,tags="ligne")
    dessindamier(n,dessin,fen)

def dessinUndoRapide(chemin,fen,dessin,n,texte): #Permet d'annuler la représentation d'un déplacement (Version Rapide)
    dessin.delete("all")
    dessindamier(n,dessin,fen)
    dessinchemin(chemin,fen,dessin)

def dessinchemin(chemin,fen,dessin,trouve=False,cycle=False): #Dessine le chemin final
    for i in range(len(chemin)-1):
        dessindeplacement(chemin[i],chemin[i+1],fen,dessin,trouve,i)
    if trouve and cycle:
        dessindeplacement(chemin[-1],chemin[0],fen,dessin,trouve,i,cycle)

def dessinNonTrouver(n,dessin,fen,texte): #Représentation du cas dans lequel aucun parcours n'est trouvé
    dessindamier(n,dessin,fen)
    dim=(n+1)*100
    dessin.create_line(50,50,dim+50,dim+50,fill='red',width=15)
    dessin.create_line(dim+50,50,50,dim+50,fill='red',width=15)
    dim = (n+1)*100
    police=font.Font(size=20)
    texte['text']="Il n'y a pas de solution !"
    texte['fg']="red"

def enCours(texte): #Génération d'un texte informatif sur l'état d'avancement
    texte['text']="Recherche en cours"
    texte['fg']="black"
    

def Trouve(texte):  #Génération d'un texte informatif sur l'état d'avancement
    texte['text']="Une solution a été trouvée !"
    texte['fg']="green"



def parcour(pos,n,affichage,rapide,cycle): #Programme Principale du parcours du damier
    fen = Tk()#Init de l'affichage
    fen.title('Tour du cavalier')#Suite de l'init
    dim = (n+1)*100 #Calcul de la dimension de l'échiquier
    impossible = False #Init de la variable pour l'impossibilité
    dessin=Canvas(fen, bg="ivory", width=dim+200, height=dim+200)#Création de la zone de dessin de l'échiquier
    dessindamier(n,dessin,fen)#Dessin du damier
    police=font.Font(size=20)#Une police pour les dessins
    texte=Label(fen,text="",fg="black",justify="center",font=police)#Texte en bas de la zone de dessin
    texte.grid(row=2)#Positionnement du texte
    enCours(texte)#set de la valuer du text
    echequier = [[0] * n for i in range(n)]#Initialisation de la matrice pour suivre si une case est visité ou non (0 : pas visité/1: visité)
    essaie = {}#Création d'un dictionaire pour le backtracking
    for i in range(n):#Pour chaque case
        for y in range(n):#Suite du pour chaque case
            essaie[(i,y)]=[]#Initialisation d'un tableau avec pour clé l'indice x et y de la case
    for i in echequier:#Affichage de la matrice dans la console
        print(i)
    chemin=[]#Init du chemin
    echequier[pos[0]][pos[1]]=1#On met le point de départ comme visité dans la matrice
    for i in echequier:#Affichage de la matrice dans la console
        print(i)
    print("-------------------------------------------")
    chemin.append(pos)#Ajout du point de départ dans le chemin
    while tourNonEffectue(echequier,cycle,chemin,n) and not impossible: #Vérification que l'on a pas fini et si il reste des possibilitées à exploré
        if voisindispo(chemin[-1],echequier,essaie[chemin[-1]]) : #Vérification de l'existence de voisins non visité
            newpos=voisindispo(chemin[-1],echequier,essaie[chemin[-1]])[0] #Attribution de la nouvelle position en prenant le premier des voisin disponible
            if affichage: #Gestion de l'affichage graphique
                dessindeplacement(chemin[-1],newpos,fen,dessin)
            chemin.append(newpos) #Ajout de la nouvelle position dans le chemin
            echequier[newpos[0]][newpos[1]]=1 #Initialisation de la nouvelle position comme visité dans la matrice
            for i in echequier: #Affichage dans la console de l'essaie
                print(i)
            print("-------------------------------------------")
        else: #Cas où aucun voisin n'est disponible
            if len(chemin)!=1:#Si il reste des points dans le chemin (Si il reste des solutions)
                dernier=chemin.pop()#Suppression du dernier point
                essaie[chemin[-1]].append((dernier))#Ajout du point dans le dictionaire dans l'avant dernier point pour enregistrer un essaie ratée
                essaie[dernier]=[]#Réinitialisation des essaie du dernier point pour pouvoir en refaire quand on reviendra sur ce point
                echequier[dernier[0]][dernier[1]]=0 #Initialisation du dernier point comme non visité dans la matrice
                if affichage: #Gestion de l'affichage graphique
                    if rapide :
                        dessinUndoRapide(chemin,fen,dessin,n,texte)
                    else:
                        dessinUndoLent(dernier,chemin[-1],fen,dessin,n)
            else: #Si il ne reste pas de solutions
                impossible=True #Alors la résolution est impossible
    if impossible: #Si impossible
        print("Il n'existe pas de solution")#Affichage console
        dessinNonTrouver(n,dessin,fen,texte)#Affichage Graphique
    else : #Si une solution à été trouvée
        print(chemin)#Affichage console
        dessinchemin(chemin,fen,dessin,True,cycle)#Affichage Graphique
        Trouve(texte)#Affichage Graphique
    fen.mainloop()

def interface(): #Création d'une interface pour lancer le parcours
    inter=Tk()
    inter.title("Le tour du Cavalier")
    text1 = Label(inter,text = 'Bonjour et bienvenue sur ce simulateur du Problème du Cavalier',anchor='center')
    text1.grid(row=0,columnspan=2)
    textvide1 = Label(inter,text="")
    textvide1.grid(column=0,row=1)
    text2 = Label(inter,text = "Veuillez entrer la dimension de l'échiquier : ")
    text2.grid(column=0,row=2,sticky='e')
    boxdim = Entry(inter,width=20)
    boxdim.grid(column=1,row=2)
    textvide2 = Label(inter,text="")
    textvide2.grid(column=0,row=3)
    text3 = Label(inter,text="Entrez la position de départ du cavalier :",anchor='center')
    text3.grid(column=0,row=4,columnspan=2)
    text4 = Label(inter,text="x :")
    text4.grid(column=0,row=5,sticky='e')
    boxPosX = Entry(inter,width=20)
    boxPosX.grid(column=1,row=5)
    text5 = Label(inter,text="y :")
    text5.grid(column=0,row=6,sticky='e')
    boxPosY = Entry(inter,width=20)
    boxPosY.grid(column=1,row=6)
    textvide3 = Label(inter,text="")
    textvide3.grid(column=0,row=7)
    text6 = Label(inter,text="Voulez suivre la recherche graphiquement ?")
    text6.grid(column=0,row=8,columnspan=2)
    selectionner=BooleanVar()
    rad1 = Radiobutton(inter,text='Oui', value=True, variable=selectionner,command=lambda:[text7.grid(),rad3.grid(),rad4.grid()])
    rad2 = Radiobutton(inter,text='Non', value=False, variable=selectionner,command=lambda:[text7.grid_remove(),rad3.grid_remove(),rad4.grid_remove()])
    rad1.grid(column=0, row=9)
    rad2.grid(column=1, row=9)
    textvide4 = Label(inter,text="")
    textvide4.grid(column=0,row=10)
    text7=Label(inter,text="Veuillez choisir la vitesse de l'affichage ( 'Lent' ralenti grandement l'éxécution )")
    text7.grid(column=0,row=11,columnspan=2)
    text7.grid_remove()
    vitesse=BooleanVar()
    rad3 = Radiobutton(inter,text='Rapide',value=True,variable=vitesse)
    rad4 = Radiobutton(inter,text='Lent',value=False,variable=vitesse)
    rad3.grid(column=0,row=12)
    rad4.grid(column=1,row=12)
    rad3.grid_remove()
    rad4.grid_remove()
    textvide6 = Label(inter,text="")
    textvide6.grid(column=0,row=13)
    text8 = Label(inter,text="Souhaitez vous trouvez un chemin fermé (Autrement dit un cycle ?)")
    text8.grid(column=0,row=14,columnspan=2)
    fermer=BooleanVar()
    rad5= Radiobutton(inter,text='Oui',value=True,variable=fermer)
    rad6 = Radiobutton(inter,text='Non',value=False,variable=fermer)
    rad5.grid(column=0,row=15)
    rad6.grid(column=1,row=15)

    textvide5 = Label(inter,text="")
    textvide5.grid(column=0,row=16)
    
    def lancement():
        posx=int(boxPosX.get())
        posy=int(boxPosY.get())
        pos=(posx,posy)
        n=int(boxdim.get())
        if n>0:
            text2['text']="Veuillez entrer la dimension de l'échiquier : "
            text2['fg']="black"
            if n>posx and n>posy:
                if posx>=0 and posy>=0:
                    affichage=selectionner.get()
                    rapide=vitesse.get()
                    cycle=fermer.get()
                    inter.destroy()
                    parcour(pos,n,affichage,rapide,cycle)
                else:
                    text4['text']="(Dois respecter cette condition 0<=x<dimension de l'échiquier) x:"
                    text5['text']="(Dois respecter cette condition 0<=y<dimension de l'échiquier) y:"
                    text4['fg']="red"
                    text5['fg']="red"
            else:
                text4['text']="(Dois respecter cette condition 0<=x<dimension de l'échiquier) x:"
                text5['text']="(Dois respecter cette condition 0<=y<dimension de l'échiquier) y:"
                text4['fg']="red"
                text5['fg']="red"
        else:
            text2['text']="Veuillez entrer la dimension de l'échiquier : \n (Condition à respecter : n>0)"
            text2['fg']="red"

    btn = Button(inter, text="Lancer La simulation", command=lancement)
    btn.grid(column=0,row=17,columnspan=2)
    inter.mainloop()

#parcour((1,1),6,False,False,False)

interface() #Lancement de script