
import sys
from  math import *
class Graphe(object):
    
	def __init__(self,n):
		self.arcs ={} # dictionnaire des arcs du graphe
		self.sommets=[] # liste des sommets du graphe
		if isinstance(n,int): # n est un int, il y aura n sommet de valeur 0 à n
			for i in range(n+1):
				self.sommets.append(i)
		elif isinstance(n,list): # n est une liste qu'on place dans sommet directement
			for i in range(len(n)):
				self.sommets.append(n[i])
		else:
			print("Votre paramètre d'entrée n'est pas compatible".center("@",50))

	# Ajoute de sommet si il n'existe pas déja dans le graphe
	#  Verification de la cohérence.(sommet type en entier)
	def Ajouter_sommet(self,sommet):
		if sommet not in self.sommets:
			if isinstance(sommet,int):
				self.sommets.append(sommet)
			else:
				print ("Sommet "+str(sommet)+" n'est pas compatible avec le graphe" )
		else:
			print("Le sommet existe déja")

	# Permet d'ajouter un arc au graphe si les deux sommets placé en paramètre existent et si l'arc n'existe pas déja.
	def Ajouter_arc(self, sm1, sm2, v=1, oriente=True):
		if sm1 in self.sommets and sm2 in self.sommets:
			if isinstance(sm1,int) and isinstance(sm2,int):
				if not (sm1,sm2) in self.arcs:
					self.arcs[(sm1,sm2)]=v
					if oriente == False:
						if not (sm2,sm1) in self.arcs:
							self.arcs[(sm2,sm1)]=v
				else:
					print (" Arc ou Arrete existe déja".center(50,'?'))
			else:
				print ("Sommet n'est pas compatible avec le graphe".center(50,'?') )
		else:
			print("Au moins 1 des deux sommets n'existe pas".center(50,'?'))

	def predecesseurs(self,sm):
		pred=[]
		for couple in self.arcs.keys():
			if couple[1]==sm:
				pred.append(couple[0])
		return pred

	def successeurs(self,sm):
		suc=[]
		for couple in self.arcs.keys():
			if couple[0]==sm:
				suc.append(couple[1])
		return suc


	# test si le graphe possède ou non des arcs négatifs
	def Arc_negatif(self):
		result=False
		for value in self.arcs.values():
			if value<0:
				result= True
		return result



##############################################################
#Implementation de l'algorithme de Bellman graphe sans circuit
##############################################################

def choisir(graphe,sinconnu,sconnu):
    """
        input : le graphe et liste de sommet inconnu(X - E) et sommet connu(Ensemble E )
        output : un sommet ayant tous ses predecesseurs dans s_connu
    """
    sommetcandidat=[]

    for sommet in sinconnu:
        pred = graphe.predecesseurs(sommet)
        if (all( x in sconnu for x in pred)):
            sommetcandidat.append(sommet)
    return sommetcandidat


#######
#fonction qui Calcul l'infini

####
#Calcul des plus long chemin : applique algo vu en cours
###
def pccBellman(graphe, s):
    """
        Parametre dentrée : objet graphe
                             le sommet s : source
        Sortie :
            d = {} : dictionnaire du pcc entre la source et un sommet i qui est la clé
            pred = {} #dictionnaire des predecesseurs dans ce pcc

        Contrainte : pas de circuit
    """

    ##Variables
    s_connu = [] #liste de sommet dont on connait la Longue courte distance(pcc)
    s_inconnu =[] #liste de sommet dont le pcc inconnu
    d = {} #dictionnaire du pcc entre la source et un sommet i qui est la clé
    pred = {} #dictionnaire des predecesseurs

    infini = -float('inf')#infini en python

    ## initialisation
    #tous les sommets sauf l'origine sont dans s_inconnu

    for vertice in graphe.sommets:
        if vertice != s:
            s_inconnu.append(vertice)

    s_connu.append(s)
    d[s]=0
    try :
        while (s_inconnu):
            sommetcandidat=choisir(graphe,s_inconnu,s_connu)
            x=min(sommetcandidat)
            s_inconnu.remove(x)
            n=infini
            for y in graphe.predecesseurs(x):
                couple=(y,x)
                np=d[y] + graphe.arcs[couple]
                if np > n :
                    z=y
                    n=np
            d[x]=n
            s_connu.append(x)
            pred[x]=z
        return d,pred
    except:
        sys.exit("L'algorithme bloque quand un sommet n'a pas de predecesseurs(sommet 0)")

######################################################
#### Extraire le plus long chemin entre deux sommets
#Si chemin existe on l'Affiche
#Sinon on envoie message d'erreur
####################################################

def BellmanXY(graphe, sm1,sm2):
    """
        param In : graphe, sommet source, sommet destination

        param out : liste =[ sm1, b, sm2] : chemin entre sm1 et sm2 si existe
                    cost : int : le cout du chemin
                        --
                     liste=[None] : si pas de chemin
                     cost = None  : ||
    """
    d,pred =pccBellman(graphe,sm1)

    liste=[]
    sommet=sm2
    cost=None #initiation valeur cout si pas de chemin
    if sommet in pred.keys():
        cost=d[sm2]
        liste.insert(0,sm2)
        for key,values in pred.items():
            if(pred[sommet] != sm1):
                sget=pred[sommet]
                liste.insert(0,sget)
                sommet=sget
        liste.insert(0,sm1)
    else:
        liste.append(None)##si pas de chemin(pas de predecesseurs)
    #print(liste)
    #print(cost)
    return liste,cost

#####################################################
## Affiche tous les plus courts chemin
#    entre le sommet source et tous les autres sommets
# !!! appel de BellmanXY (voir fonction dessus)
#################

def Bellman(graphe,s):
    """
        param In : graphe et sommet source

        Sortie : Affiche les pcc entre la source et les sommets du graphe

        !!! appel de BellmanXY(voir fonction dessus)
    """
    chemins={} # dictionnaire des chemins
    #clé : longueur chemin
    #valeur: liste des chemins entre  S et les sommets du graphe

    print('*'*50)
    print("Recherche du plus long chemin entre {} et tous les autres sommets".format(s))
    print("*"*50)
    print('Plus long chemin de : ')
    sommets_injoignable=[] # on stocke les sommets injoignables
    i = 0
    for sommet in graphe.sommets:
        if sommet !=s:
            listd,cost=BellmanXY(graphe,s,sommet)
            if cost !=None:
                chemins[cost]=listd
                for keys,values in chemins.items():
                    print("itration "+str(i)+" longueur ", keys, " :", '->'.join(map(str,values)))
                chemins={}
            else :
                sommets_injoignable.append(sommet)
        i+=1
    for k in sommets_injoignable:
        print("il ny a aucun chemin de {} à {} ".format(s,k))

##################### Tests de Bellman #############################

print("creation du graphe".center(50,"*"))
print()
g= Graphe(5)
g.Ajouter_arc(0,1,1)
g.Ajouter_arc(0,2,-2)
g.Ajouter_arc(1,3,-2)
g.Ajouter_arc(1,5,3)
g.Ajouter_arc(2,1,1)
g.Ajouter_arc(2,3,5)
g.Ajouter_arc(2,4,4)
g.Ajouter_arc(4,5,-1)
g.Ajouter_arc(5,3,-5)
print()


print("Test de Bellman sur graphe (pas de circuit)".center(50,"*"))
print()
Bellman(g,0)
print()
