import operator
import random

#courant est un état donc une liste des positions de tous les éléments de taquin
#ouverte = liste qui contient les états examinés au cours du parcours
#fermée = liste des états retenus (ceux dont le coût f () est le plus bas)

##################################
#Fonctions nécessaires au fonctionnement de l'algorithme A*
##################################

###########
## Renvoie liste du nombre de déplacements élémentaires de chaque éléments
def epsilon(sommet, liste): 
    config = sommet[0]
    epsilon = []
    ## Comparaison de l'index de chaque élément entre la configuration actuelle (config) et la configuration finale (liste)
    for i in liste:
        if(liste.index(i)>config.index(i)):
            e = liste.index(i)-config.index(i)
        elif(liste.index(i)<config.index(i)):
            e = config.index(i)-liste.index(i)
        else:
            e = 0
        
        epsilon.append(e)
    return epsilon

###########
## Calcule la somme pondérée réduite des distances élémentaires d'un sommet en fonction d'une heuristique choisie
def h(sommet, heuristique):
    pi1_6 = [[36,12,12,4,1,1,4,1,0], [8,7,6,5,4,3,2,1,0], [8,7,6,5,3,2,4,1,0], [1,1,1,1,1,1,1,1,0]]
    rho1_6 = [4, 1]
    liste = [0,1,2,3,4,5,6,7,"X"]
    h = 0
    e = epsilon(sommet, liste)

    if(heuristique==6):
        pi = pi1_6[3]
        rho = rho1_6[1]
    elif(heuristique==1):
        pi = pi1_6[0]
        rho = rho1_6[0]
    elif(heuristique==2):
        pi = pi1_6[1]
        rho = rho1_6[1]
    elif(heuristique==3):
        pi = pi1_6[1]
        rho = rho1_6[0]
    elif(heuristique==4):
        pi = pi1_6[2]
        rho = rho1_6[1]
    else:
        pi = pi1_6[2]
        rho = rho1_6[0]
            
    for i in range(0,9):
        h = h + pi[i]*e[i]
            
    return h/rho

###########
## Calcule le nombre de changement de configuration d'un sommet à partir de la configuration initial
def g(sommet):
    chemin = sommet[1]
    g = len(chemin)
    return g

###########
## Renvoie une liste d'état sucesseurs de notre état courant (= états accessibles depuis notre état courant)
def successeurSommet(courant):
    
    # Intitialisation de la liste listSucc qui contiendra les états successeurs
    listSucc = []

    # Stockage de l'index où est positionné le trou "X"
    n = courant[0].index("X")

    # Création de nouveaux vecteurs représentant les configurations accessibles depuis notre configuration courante,
    # selon la position du trou dans le puzzle.
    if(n==0): # dans le coin gauche en haut
        listSucc.append(configDroite(courant, n))
        listSucc.append(configBas(courant, n))
       
    elif(n==1): # centré en haut 
        listSucc.append(configDroite(courant, n))
        listSucc.append(configBas(courant, n))
        listSucc.append(configGauche(courant, n))
        
    elif(n==2): # dans le coin droit en haut
        listSucc.append(configBas(courant, n))
        listSucc.append(configGauche(courant, n))

    elif(n==3): # centré à gauche
        listSucc.append(configHaut(courant, n))
        listSucc.append(configDroite(courant, n))
        listSucc.append(configBas(courant, n))

    elif(n==4): # au centre du puzzle
        listSucc.append(configHaut(courant, n))
        listSucc.append(configDroite(courant, n))
        listSucc.append(configBas(courant, n))
        listSucc.append(configGauche(courant, n))

    elif(n==5): # centré à droite
        listSucc.append(configHaut(courant, n))
        listSucc.append(configBas(courant, n))
        listSucc.append(configGauche(courant, n))

    elif(n==6): # dans le coin gauche en bas
        listSucc.append(configHaut(courant, n))
        listSucc.append(configDroite(courant, n))

    elif(n==7): # centré en bas
        listSucc.append(configGauche(courant, n))
        listSucc.append(configHaut(courant, n))
        listSucc.append(configDroite(courant, n))

    else: # dans le coin droit en bas
        listSucc.append(configGauche(courant, n))
        listSucc.append(configHaut(courant, n))

    return listSucc

###########
## Les 4 fonctions de changement de configuration à partir du sommet donné et élaboration du chemin
## Ce changement de configuration se fait avec le déplacement du trou (permutation entre le trou et un élément)
def configDroite(courant, index):

    # Copie de la configuration de notre état courant dans une liste "liste"
    liste = courant[0]
    succ_droite = liste[:]
    aux = succ_droite[index]
    succ_droite[index] = succ_droite[index+1]
    succ_droite[index+1] = aux

    chemin = courant[1] + "E"                   
    return [succ_droite, chemin, 0]

def configGauche(courant, index):
    liste = courant[0]
    succ_gauche = liste[:]
    aux = succ_gauche[index]
    succ_gauche[index] = succ_gauche[index-1]
    succ_gauche[index-1] = aux

    chemin = courant[1] + "O"                   
    return [succ_gauche, chemin, 0]

def configBas(courant, index):
    liste = courant[0]
    succ_bas = liste[:]
    aux = succ_bas[index]
    succ_bas[index] = succ_bas[index+3]
    succ_bas[index+3] = aux

    chemin = courant[1] + "S"                   
    return [succ_bas, chemin, 0]

def configHaut(courant, index):
    liste = courant[0]
    succ_haut = liste[:]
    aux = succ_haut[index]
    succ_haut[index] = succ_haut[index-3]
    succ_haut[index-3] = aux

    chemin = courant[1] + "N"                   
    return [succ_haut, chemin, 0]

##################################
# Algorithme
##################################

def algo_A(s, t, heuristique):
    # ouverte
    # fermée : file d'attente
    trouvé = False
    f = h(s, heuristique)
    s[2] = f
    ouverte = [s]
    fermée = []
    cpt = 0
    while(trouvé == False):
        #retirer le meilleur sommet de ouverte et l'ajouter dans fermée
        #on expanse tous les successeurs de l'état/sommet d'ouverte
        #et on enlève le meilleur = courant, celui qui va devenir notre actuel

        ouverte = sorted(ouverte, key=operator.itemgetter(2))
        ##courant = meilleurSommet(ouverte)

        courant = ouverte[0]
        ouverte.remove(courant)
        fermée.append(courant)
        
        if (courant[0]==t): # si le meilleur noeud est égal au noeuf final (notre but) : trouvé prend la valeur True
            trouvé = True
        else :
            #poursuivre la recherche du chemin
            for succ in successeurSommet(courant):
                f = g(succ) + h(succ,heuristique) # Numéro de l'heuristique choisi en paramètre de appel fonction h(sommet, numHeuristique)
                succ[2] = f

                absent = True
                for e in fermée:
                    if(succ[0]==e[0]):
                        absent = False
                        index = fermée.index(e)
            
                if(absent):
                    # succ n'est pas présent dans fermée
                    ouverte.append(succ)
                else:
                    #succ déjà présent dans fermée (absent = False)
                    aux = fermée[index]
                    if (succ[2]<aux[2]):
                        fermée.remove(aux)
                        ouverte.append(succ)
            #tous les successeurs de courant ont été traités
    #on quitte le while
    print("Configuration finale : ", courant[0])
    print("Chemin : ",courant[1])
    print("Longueur du chemin = ", len(courant[1]), " déplacements")
#fin de l'algorithme A*

##################################
# Menu
##################################

###########
## Fonction de vérification si le jeu est résolvable à partir d'une configuration
## initiale prise en paramètre
def verif_resolution(sommet, liste):
    config = sommet[0]
    verif =  config[:]
    cpt = 0
    cptX = 0
    x = "X"

    # calcule la distance élémentaire de la case vide
    if(liste.index(x)>verif.index(x)):
        cptX = liste.index(x)-verif.index(x)
    elif(liste.index(x)<verif.index(x)):
        cptX = verif.index(x)-liste.index(x)
    else:
        cptX = 0

    # calcule nombre de permutations à réaliser pour atteindre l'état final
    for i in liste:
        if(verif.index(i)!=liste.index(i)):
            aux = verif[verif.index(i)]
            verif[verif.index(i)]= verif[liste.index(i)]
            verif[liste.index(i)] = aux
            cpt = cpt + 1

    # la parité doit être égale pour les deux compteurs, sinon la résolution
    # du problème est impossible
    if(cptX%2!=cpt%2):
        return False
    else:
        return True

###########
## Retourne une configuration initiale générée automatiquement
def config_auto(liste):
    list = liste[:]
    config = []
    for i in range(len(list)):
        e = random.choice(list)
        config.append(e)
        list.remove(e)
    return config

###########
## Permet d'appeler l'algorithme A* en fonction du ou des heuristiques choisie(s)
def choixHeuristique(s, t):
    print("Choix de l'heuristique :")
    print("1 : Faire tourner l'algorithme avec une seule heuristique")
    print("2 : Tester toutes les heuristiques pour une même configuration")
    choix = input()
    
    if(choix=="1"):
        print("Entrez le numero de l'heuristique choisie (1 à 6) :")
        h = input()
        algo_A(s, t, h)
        
    elif(choix=="2"):
        for i in range(1, 7):
            print("\nHeuristique ",i,":")
            algo_A(s, t, i)
        print("L'algorithme a tourné avec les 6 heuristiques enregistrées")

###########
## Appelle le menu qui permet de choisir les conditions d'appel de l'algorithme
def Menu():
    t = [0,1,2,3,4,5,6,7,"X"]   #Etat final

    menu = True
    print("\nBienvenue au jeu du taquin !")
    print("Le but du jeu est de choisir ou de générer une configuration initiale puis de laisser l'algorithme se dérouler, nous permettant de récuperer le chemin qui nous aura amené à l'état final.")
    while(menu):
        print("\nVeuillez choisir une des options suivantes :")
        print("1 : Générer une configuration automatiquement")
        print("2 : Entrer sa propre configuration initiale")
        print("3 : Sortir du programme")
        
        choixInitial = input()
              
        if(choixInitial=="1"):
            s = [[], "", 0]
            s[0] = config_auto(t)
            while(verif_resolution(s, t)==False):
                print("La configuration n'est pas résoluble")
                s[0] = config_auto(t)
            print("Voici la configuration initiale générée :", s[0])
            choixHeuristique(s, t)
            
        elif(choixInitial=="2"):
            s = [[], "", 0]
            entrée = True
            while(entrée):
                print("Entrez votre configuration élément par élément dans l'ordre souhaité.")
                print('Exemple : 1 puis 3 puis "X" puis 5 etc... pour une liste [1,3,"X",5,7,6,4,2,0]')
                print("  1  3  X")
                print("  5  7  6")
                print("  6  4  2")
                config_s = []
                
                for i in range(0,9):
                    e = input()
                    if(e=="X"):
                        nbr = e
                    else:
                        nbr = int(e)
                    config_s.append(nbr)
                    
                s[0] = config_s
                if(verif_resolution(s, t)):
                    print("Voici votre configuration finale : ", s[0])
                    choixHeuristique(s, t)
                    entrée = False
                else:
                    print("Votre configuration n'a pas de solution possible, veuillez en sélectionner une autre")
            
        elif(choixInitial=="3"):
            print("Vous êtes bien sortis du programme")
            menu = False
            
        else:
            print("Votre choix n'est pas conforme.")
            

##################################
# Main
##################################

Menu()


























                    
                
                

        
    
    
    
    
