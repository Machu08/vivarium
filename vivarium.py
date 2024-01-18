# -- coding: utf-8 --
# Importation des modules

from tkinter import *
import numpy as np
import random as rd
from pygame import *
import time
import matplotlib.pyplot as plt
import math

### Caractéristiques du monde ###

taille_vivarium =20
global nombre_vegetaux
global nombre_herbivores
global nombre_carnivores
global nombre_jours
global nombre_jours_liste
nombre_jours, nombre_jours_liste = 0, [0]
nombre_vegetaux_liste, nombre_herbivores_liste, nombre_carnivores_liste = [], [], []

### On définit les listes de paramètres qui seront réutilisés ###

## Végétaux ##

maladies_vegetaux = ['non malade', 'malade']
types_vegetaux = ['céréale', 'chêne', 'herbe']
type_cereale = [[0], 9 * 30, 0.6, 1.5, 0.9, [0], [12, 25], maladies_vegetaux, 1, 6]
type_chene = [[0], 800 * 360, 0.1, 1, 0, 0.10, [-5, 30], maladies_vegetaux, 800, 1]
type_herbe = [[0, 1], 100 * 360, 0.8, 1, 0, 0.005, [-15, 40], maladies_vegetaux, 0.5, 7]
# type_"vegetaux"=[[substrat],durée de vie, capacité de repro, besoin en eau, besoin en lumiere,quantité de sels nécessaires, plage de temperature, maladies possibles,masse,valeur nutritive]
types_vegetaux2 = [type_cereale, type_chene, type_herbe]
nombre_vegetaux = 200
couleurs_vegetaux = ['#3B823D', '#0B3A04', '#06AA09']

## Herbivores ##

maladies_herbivores = ['non malade', 'malade']
types_herbivores = ['lapin', 'campagnol']
type_lapin = [2 * 360, 0.6, 0.5, 8, [0, 2], maladies_herbivores, 1.8, 450, 3]
type_campagnol = [360, 0.9, 0.3, 12, [0], maladies_herbivores, 0.6, 120, 3]
# type_herbivore = [durée de vie, capacité de reproduction,besoin en eau,nombre d'enfants par porté,regime alimentaire(type de vegetaux),maladies possibles, masses, valeur nutritive)
types_herbivores2 = [type_lapin, type_campagnol]
nombre_herbivores = 50
couleurs_herbivores = ['#5A024C', '#EC1DC9']

## Carnivores ##

maladies_carnivores = ['non malade', 'malade']
types_carnivores = ['buse', 'renard']
type_buse = [24 * 360, 0.4, 0.4, 700, [0, 1], maladies_carnivores, 4.5, 120, 9, 2]
# type_carnivore = [durée de vie, capacité de reproduction, besoin en eau, besoin nutritif, regime alimentaire, maladies, masse maximum,??,déplacements possible, nombre de proies par jour]
type_renard = [5 * 360, 0.6, 0.3, 600, [0, 1], maladies_carnivores, 2.8, 450, 6, 1]
types_carnivores2 = [type_buse, type_renard]
nombre_carnivores = 20
couleurs_carnivores = ['#480304', '#E30206']

## Terrain ##

substrats = ['argile', 'sable', 'eau']
couleurs_substrats = ['#CF670C', '#BDC308', 'navy']

## Date ##

mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre',
        'décembre']
global annee_actuelle
global mois_actuel
global jour_actuel
saison_actuelle = 3
annee_actuelle = 1
mois_actuel = 1
jour_actuel = 1

## Saison ##

printemps = [0.4, 10, [8, 19], 'printemps']
ete = [0.1, 10, [10, 30], 'été']
automne = [0.6, 10, [5, 15], 'automne']
hiver = [0.7, 10, [-5, 10], 'hiver']
saisons = [printemps, ete, automne, hiver]
# saison=[probabilité de pluie pour un jour, quantité de pluie pour une case en L]

### Fonctions d'utilité générale ###

def fusionner(L1, L2):
    if len(L1) == 0:
        return L2
    elif len(L2) == 0:
        return L1
    else:
        i = 0
        j = 0
        L3 = []
        while len(L3) < (len(L1) + len(L2)):
            if i > len(L1) - 1:
                for k in range(j, len(L2)):
                    L3.append(L2[k])
            elif j > len(L2) - 1:
                for k in range(i, len(L1)):
                    L3.append(L1[k])
            else:
                if L1[i] <= L2[j]:
                    L3.append(L1[i])
                    i += 1
                else:
                    L3.append(L2[j])
                    j += 1
    return L3

def tf(L):
    if len(L) < 2:
        return L
    else:
        L1 = L[0:len(L) // 2]
        L2 = L[len(L) // 2:len(L)]
    return fusionner(tf(L1), tf(L2))

### Fonctions de création du vivarium ###

## Création générale du terrain ##

def creation_vivarium_terrain(substrats):
    global vivarium_terrain
    vivarium_terrain = np.zeros([taille_vivarium, taille_vivarium, 4], dtype=np.uint8)
    vivarium_terrain_elargi = np.zeros([taille_vivarium + 2, taille_vivarium + 2, 1], dtype=np.uint8)
    vivarium_terrain_moyenne = np.zeros([taille_vivarium, taille_vivarium, 1], dtype=np.uint8)
    eau = rd.randint(0, 100)
    temperature = rd.randint(8, 19)
    # On créer une matrice vivarium terrain plus grande de 2 cases en longueur et en largeur et on attribue à chaque case une valeur de substrat aléatoire
    for colonne in range(taille_vivarium + 2):
        for ligne in range(taille_vivarium + 2):
            vivarium_terrain_elargi[ligne][colonne][0] = rd.randint(0, 1)
    # On attribue à case du vivarium terrain une valeur de température et une quantité d'eau (uniques) ainsi qu'une valeur en éléments minéraux aléatoire
    for ligne1 in range(taille_vivarium):
        for colonne1 in range(taille_vivarium):
            vivarium_terrain[ligne1][colonne1][1] = eau
            vivarium_terrain[ligne1][colonne1][2] = temperature
            vivarium_terrain[ligne1][colonne1][3] = rd.randint(1000, 2000)
            for x in range(-1, 2):
                for y in range(-1, 2):
                    vivarium_terrain_moyenne[ligne1][colonne1] += \
                        vivarium_terrain_elargi[ligne1 + 1 + x][colonne1 + 1 + y][0]
    # On attribue une valeur de substrat à chaque case du vivarium terrain non élargi en fonction des substrats l'entourant pour avoir des surfaces cohérentes
    for ligne2 in range(taille_vivarium):
        for colonne2 in range(taille_vivarium):
            if vivarium_terrain_moyenne[ligne2][colonne2] >= 5:
                vivarium_terrain[ligne2][colonne2][0] = 1
            else:
                vivarium_terrain[ligne2][colonne2][0] = 0
    creation_riviere()
    return vivarium_terrain

## Fonctions de création des surfaces aquatiques ##

def surface_aquatique():
    global vivarium_terrain
    #On appelle ici la fonction qui créer une rivière sur le vivarium
    vivarium_terrain = creation_riviere()
    return vivarium_terrain

def creation_riviere():
    global vivarium_terrain
    source_ligne = 0
    source_colonne = rd.randint(1, taille_vivarium - 2)
    vivarium_terrain[0][source_colonne][0] = 2
    # Ici on place une case d'eau aléatoire sur la première ligne du vivarium terrain
    # Puis on place des cases d'eau aléatoires avec pour condition un côté touchant un côté de la précédente
    # et une plus grande probabilité de se trouver en dessous que sur le côté
    while 0 <= source_ligne < taille_vivarium - 1 and 0 <= source_colonne < taille_vivarium - 1:
        prochaine_case_ligne = rd.randint(1, 3)
        prochaine_case_colonne = rd.randint(1, 3)
        if prochaine_case_ligne == 1:
            source_ligne2 = source_ligne
        elif prochaine_case_ligne != 1:
            source_ligne2 = source_ligne + 1
        if prochaine_case_colonne == 1:
            source_colonne2 = source_colonne + rd.choice([-1, 1])
        elif prochaine_case_colonne != 1:
            source_colonne2 = source_colonne
        if source_ligne == source_ligne2 or source_colonne == source_colonne2:
            vivarium_terrain[source_ligne2][source_colonne2][0] = 2
            source_ligne, source_colonne = source_ligne2, source_colonne2

## Mise en place des végétaux ##

def creation_vivarium_vegetaux(taille_vivarium, couleurs_vegetaux, maladies_vegetaux, nombre_vegetaux, types_vegetaux):
    global vivarium_vegetaux
    global presence_vegetaux
    vivarium_vegetaux = np.zeros([taille_vivarium, taille_vivarium, 4], dtype=np.uint8)
    presence_vegetaux = []
    quota = nombre_vegetaux
    # On place sur le vivarium végétaux un nombre de végétaux dépendant d'un quota défini au début du programme en leur
    # attribuant à chaque fois un type aléatoire, un âge de 10 ans (car ils ne peuvent être dévorer qu'à partir de cet âge)
    # la présence ou non de maladie et
    while quota > 0:
        ligne, colonne = rd.randint(0, taille_vivarium - 1), rd.randint(0, taille_vivarium - 1)
        presence_truefalse = [ligne, colonne] in presence_vegetaux
        if presence_truefalse == False:
            vivarium_vegetaux[ligne][colonne][1] = rd.randint(0, len(types_vegetaux) - 1)
            type = vivarium_vegetaux[ligne][colonne][1]
            if verification_substrat(ligne, colonne, type):
                # On vérifie ici si le substrat sur lequel s'installe le végétal lui est adapté, sinon on vide la case
                vivarium_vegetaux[ligne][colonne][2] = 10
                vivarium_vegetaux[ligne][colonne][0] = rd.randint(0, len(maladies_vegetaux) - 1)
                presence_vegetaux += [[ligne, colonne]]
                vivarium_vegetaux[ligne][colonne][3]= 10
                quota = quota - 1
            else:
                vivarium_vegetaux[ligne][colonne][1] = 0
    return vivarium_vegetaux, presence_vegetaux

## Mise en place des animaux herbivores ##

def creation_vivarium_herbivores(taille_vivarium, couleurs_herbivores, maladies_herbivores, nombre_herbivores,
                                 types_herbivores):
    global vivarium_herbivores
    global presence_herbivores
    vivarium_herbivores = np.zeros([taille_vivarium, taille_vivarium, 5], dtype=np.uint8)
    presence_herbivores = []
    quota = nombre_herbivores
    # On place sur le vivarium herbivores un nombre de herbivores dépendant d'un quota défini au début du programme en leur
    # attribuant à chaque fois aléatoirement une maladie ou non, un type aléatoire, une masse de 0 pour débuter, un âge de 10 ans
    # (car ils ne peuvent être dévorer qu'à partir de cet âge) et un sex aléatoirement (1=femelle,0=mâle)
    while quota > 0:
        ligne, colonne = rd.randint(0, taille_vivarium - 1), rd.randint(0, taille_vivarium - 1)
        presence_truefalse = [ligne, colonne] in presence_herbivores
        if presence_truefalse == False and verification_eau(ligne, colonne):
            vivarium_herbivores[ligne][colonne][0] = rd.randint(0, len(maladies_herbivores) - 1)
            vivarium_herbivores[ligne][colonne][1] = rd.randint(0, len(types_herbivores) - 1)
            vivarium_herbivores[ligne][colonne][2] = 0
            vivarium_herbivores[ligne][colonne][3] = 10
            vivarium_herbivores[ligne][colonne][4] = rd.randint(0, 1)
            quota = quota - 1
            presence_herbivores += [[ligne, colonne]]
    return vivarium_herbivores, presence_herbivores

## Mise en place des animaux carnivores ##

def creation_vivarium_carnivores(taille_vivarium, couleurs_carnivores, maladies_carnivores, nombre_carnivores,
                                 types_carnivores):
    global vivarium_carnivores
    global presence_carnivores
    vivarium_carnivores = np.zeros([taille_vivarium, taille_vivarium, 5], dtype=np.uint8)
    presence_carnivores = []
    quota = nombre_carnivores
    # On place sur le vivarium carnivores un nombre de carnivores dépendant d'un quota défini au début du programme en leur
    # attribuant à chaque fois aléatoirement une maladie ou non, un type aléatoire, une masse de 0 pour débuter, un âge de 10 ans
    # (car ils ne peuvent être dévorer qu'à partir de cet âge) et un sex aléatoirement (1=femelle,0=mâle)
    while quota > 0:
        ligne, colonne = rd.randint(0, taille_vivarium - 1), rd.randint(0, taille_vivarium - 1)
        presence_truefalse = [ligne, colonne] in presence_carnivores
        if presence_truefalse == False and verification_eau(ligne, colonne):
            vivarium_carnivores[ligne][colonne][0] = rd.randint(0, len(maladies_carnivores) - 1)
            vivarium_carnivores[ligne][colonne][1] = rd.randint(0, len(types_carnivores) - 1)
            vivarium_carnivores[ligne][colonne][2] = 0
            vivarium_carnivores[ligne][colonne][3] = 10
            vivarium_carnivores[ligne][colonne][4] = rd.randint(0, 1)
            quota = quota - 1
            presence_carnivores += [[ligne, colonne]]
    return vivarium_carnivores, presence_carnivores

def verification_eau(colonne, ligne):
    global vivarium_terrain
    return vivarium_terrain[ligne][colonne][0] != 2

### Fonctions d'entretien ###

## Entretien terrain ##

def entretien_terrain():
    global vivarium_terrain
    vivarium_terrain = vivarium_meteo()
    return vivarium_terrain

def vivarium_meteo():
    global vivarium_terrain
    # On met à jour l'eau dans le sol (apportée par la pluie), la température de chaque case
    vivarium_terrain = vivarium_pluie()
    vivarium_terrain = vivarium_temperature()
    return vivarium_terrain

def vivarium_pluie():
    global vivarium_terrain
    global saison_actuelle
    # On lance un épisode de pluie en fonction de sa probabilité selon la saison
    if rd.random() <= saisons[saison_actuelle][0]:
        for ligne in range(taille_vivarium):
            for colonne in range(taille_vivarium):
                vivarium_terrain[ligne][colonne][1] += saisons[saison_actuelle][1]
    return vivarium_terrain

def vivarium_temperature():
    global vivarium_terrain
    global presence_vegetaux
    # On met à jour la température pour chaque case avec une température prise dans un intervale dépendant de la saison
    temperature_globale = rd.randint(saisons[saison_actuelle][2][0], saisons[saison_actuelle][2][1])
    difference_temperature_ombre = rd.randint(3, 4)
    for ligne in range(taille_vivarium):
        for colonne in range(taille_vivarium):
            vivarium_terrain[ligne][colonne][2] = temperature_globale
    # Puis on abaisse la température sous les arbre donc seulement les chênes de 3 a 4 degrées (valeur num vu dans une étude)
    for k in range(len(presence_vegetaux)):
        if vivarium_vegetaux[presence_vegetaux[k][0]][presence_vegetaux[k][1]][2] == 1:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if -1 < ((presence_vegetaux[k][0]) + x) < taille_vivarium and -1 < (
                                (presence_vegetaux[k][1]) + y) < taille_vivarium:
                        vivarium_vegetaux[(presence_vegetaux[k][0]) + x][(presence_vegetaux[k][1]) + y][
                            2] = temperature_globale - difference_temperature_ombre
    return vivarium_terrain

## Entretien vegetaux ##

def entretien_vegetaux():
    global vivarium_vegetaux
    global presence_vegetaux
    # On vérifie si les conditions de vie du végétaux sont respectées, si oui on lance reproduction et nutrition sinon on l'ajoute à la liste à tuer
    Liste_des_vegetaux_a_tuer_a_la_fin_du_cycle = []
    for k in range(len(presence_vegetaux)):
        ligne, colonne = presence_vegetaux[k][0], presence_vegetaux[k][1]
        vivarium_vegetaux[ligne][colonne][2] += 1
        if verification_vegetaux(ligne, colonne):
            reproduction_vegetaux(ligne, colonne)
            nutrition_vegetaux(ligne, colonne)
        else:
            Liste_des_vegetaux_a_tuer_a_la_fin_du_cycle += [k]
    # Puis on élimine tous les vegetaux n'ayant pas passés la vérification (les éliminer avant auraient perturbé le cycle), la liste de végétaux à tuer est strictement croissante par sa construction, ainsi, pour ne pas occasionner d'erreurs on élimines les végétaux dans l'ordre décroissant.
    Nb_Veg_Tuer = len(Liste_des_vegetaux_a_tuer_a_la_fin_du_cycle)
    for k in range(Nb_Veg_Tuer):
        mort_vegetaux(Nb_Veg_Tuer - 1 - Liste_des_vegetaux_a_tuer_a_la_fin_du_cycle[k])

def nutrition_vegetaux(ligne, colonne):
    global vivarium_vegetaux
    global presence_vegetaux
    global vivarium_terrain
    # Le végétal prélève dans son milieu les nutriments nécessaires
    vivarium_vegetaux[ligne][colonne][3] += types_vegetaux2[vivarium_vegetaux[ligne][colonne][1]][5]
    vivarium_terrain[ligne][colonne][3] -= types_vegetaux2[vivarium_vegetaux[ligne][colonne][1]][5]

def verification_vegetaux(ligne, colonne):
    # Cette fonction a pour but de vérifier que le végétal étudié n'est: ni trop vieux, ni sur un sol trop pauvre
    global vivarium_vegetaux
    type = vivarium_vegetaux[ligne][colonne][1]
    if vivarium_vegetaux[ligne][colonne][2] >= types_vegetaux2[type][1] or vivarium_terrain[ligne][colonne][3] <= \
            types_vegetaux2[type][5]:
        return False
    return True

def mort_par_predation_vegetaux(k):
   # La masse du végétal est divisée en une partie pour le prédateur et une partie retournant au sol
    global vivarium_herbivores
    global presence_vegetaux
    global vivarium_vegetaux
    global vivarium_terrain
    ligne = presence_herbivores[k][0]
    colonne = presence_herbivores[k][1]
    vivarium_herbivores[ligne][colonne][2] += 0.1 * vivarium_vegetaux[ligne][colonne][3]
    vivarium_terrain[ligne][colonne][3] += 0.9 * vivarium_vegetaux[ligne][colonne][3]
    vivarium_vegetaux[ligne][colonne] = [0, 0, 0, 0]
    presence_vegetaux.remove([ligne, colonne])

def mort_vegetaux(k):
    # le végétal est tué et remplacer par une liste de ces caractères à l'état initial et le terrain à sa place absorbe des nutriments en provenant
    global vivarium_vegetaux
    global presence_vegetaux
    global vivarium_terrain
    ligne = presence_vegetaux[k][0]
    colonne = presence_vegetaux[k][1]
    vivarium_terrain[ligne][colonne][3] += int(vivarium_vegetaux[ligne][colonne][3])
    vivarium_vegetaux[ligne][colonne] = [0, 0, 0, 0]
    del presence_vegetaux[k]

def reproduction_vegetaux(ligne, colonne):
    # Cette fonction sert à créer un nouveau végétal proche de son parent, sur un substrat adapté à son type
    global vivarium_vegetaux
    global presence_vegetaux
    global vivarium_terrain
    chance_repro = rd.random()
    type = vivarium_vegetaux[ligne][colonne][1]
    maladie = vivarium_vegetaux[ligne][colonne][0]
    for i in range(types_vegetaux2[type][9]):
        if chance_repro <= types_vegetaux2[type][2]:
            ligne1 = ligne
            colonne1 = colonne
            ligne1 += rd.randint(-1, 2)
            colonne1 += rd.randint(-1, 2)
            presence_vegetaux_truefalse = [ligne1, colonne1] in presence_vegetaux
            if 0 <= ligne1 <= taille_vivarium - 1 and 0 <= colonne1 <= taille_vivarium - 1 and presence_vegetaux_truefalse == False and verification_substrat(
                    ligne1, colonne1, type):
                presence_vegetaux += [[ligne1, colonne1]]
                vivarium_vegetaux[ligne1][colonne1] = [maladie, type, 0, 10]

def verification_substrat(colonne, ligne, type):
    if vivarium_terrain[ligne][colonne][0] in types_vegetaux2[type][0]:
        return True
    return False

## Entretien herbivores ##

def entretien_herbivores():
    global vivarium_herbivores
    global presence_herbivores
    Liste_des_herbivores_a_tuer_a_la_fin_du_cycle = []
    for k in range(len(presence_herbivores)):
        ligne, colonne = presence_herbivores[k][0], presence_herbivores[k][1]
        type = vivarium_herbivores[ligne][colonne][1]
        vivarium_herbivores[ligne][colonne][3] += 1
        Cherche_Nour = recherche_nourriture_herbivores(k, type)
        if Cherche_Nour:
            Liste_des_herbivores_a_tuer_a_la_fin_du_cycle += [k]
            # On commence par faire se déplacer l'herbivore sur le végétal le plus proche correspondant à son alimentation favorite
        elif verification_herbivores(ligne, colonne, type):
            mort_par_predation_vegetaux(k)
            reproduction_herbivores(ligne, colonne, type)
        else:
            Liste_des_herbivores_a_tuer_a_la_fin_du_cycle += [k]
    # Puis on élimine tous les herbivores n'ayant pas passés la vérification ou trouvé de nourriture (les éliminer avant auraient perturbé le cycle).
    Nb_Herb_Tuer = len(Liste_des_herbivores_a_tuer_a_la_fin_du_cycle)
    for k in range(Nb_Herb_Tuer):
        mort_herbivore_naturelle(Nb_Herb_Tuer - 1 - Liste_des_herbivores_a_tuer_a_la_fin_du_cycle[k])

def verification_herbivores(ligne, colonne, type):
    global vivarium_herbivores
    # On vérifie si l'herbivore n'est pas trop vieux
    return types_herbivores2[type][0] >= vivarium_herbivores[ligne][colonne][3]

def recherche_nourriture_herbivores(k, type):
    D = []
    global presence_herbivores
    global presence_vegetaux
    global vivarium_herbivores
    global vivarium_vegetaux
    LH = presence_herbivores
    LV = presence_vegetaux
    # On créer une liste comportant la distance et les coordonnées du végétal mangeable par l'herbivore le plus proche puis il se déplace dessus et le mange
    Dmin = []
    for vegetaux in range(len(LV)):
        ligne, colonne = presence_vegetaux[vegetaux][0], presence_vegetaux[vegetaux][1]
        x = abs(LH[k][0] - LV[vegetaux][0])
        y = abs(LH[k][1] - LV[vegetaux][1])
        if x <= types_herbivores2[type][8] and y <= types_herbivores2[type][8] and vivarium_vegetaux[colonne][ligne][
            2] >= 2:
            D += [[(x ** 2 + y ** 2) ** 0.5, LV[vegetaux][0], LV[vegetaux][1], vegetaux]]
    if D == []:
        return True
    Dmin = D[0]
    for i in range(len(D)):
        if math.floor(D[i][0]) <= Dmin[0]:
            Dmin = D[i]
    ligne_ini, colonne_ini = presence_herbivores[k][0], presence_herbivores[k][1]
    presence_herbivores[k][0] = Dmin[1]
    presence_herbivores[k][1] = Dmin[2]
    ligne, colonne = presence_herbivores[k][0], presence_herbivores[k][1]
    vivarium_herbivores[ligne][colonne] = vivarium_herbivores[ligne_ini][colonne_ini]
    vivarium_herbivores[ligne_ini][colonne_ini] = [0, 0, 0, 0, 0]
    return D == []

def reproduction_herbivores(ligne, colonne, type):
    global vivarium_herbivores
    global presence_herbivores
    # Cette fonction sert à créer un nouvel herbivore proche de son parent
    maladie = vivarium_herbivores[ligne][colonne][0]
    for i in range(types_herbivores2[type][3]):
        chance_repro = rd.random()
        if chance_repro <= types_herbivores2[type][2]:
            ligne1 = ligne
            colonne1 = colonne
            ligne1 += rd.randint(-1, 2)
            colonne1 += rd.randint(-1, 2)
            presence_herbivores_truefalse = [ligne1, colonne1] in presence_herbivores
            if 0 <= ligne1 <= taille_vivarium - 1 and 0 <= colonne1 <= taille_vivarium - 1 and presence_herbivores_truefalse == False and verification_eau(
                    ligne1, colonne1):
                presence_herbivores += [[ligne1, colonne1]]
                vivarium_herbivores[ligne1][colonne1] = [maladie, type, 0, 0, rd.randint(0, 1)]

def mort_par_predation_herbivore(k):
    # La masse de l'herbivore est divisée en deux partie, une assimilée par le carnivore et une retournant au sol
    global vivarium_herbivores
    global presence_herbivores
    global vivarium_carnivores
    global presence_carnivores
    global vivarium_terraine
    ligne = presence_carnivores[k][0]
    colonne = presence_carnivores[k][1]
    vivarium_carnivores[ligne][colonne][2] += 0.1 * vivarium_herbivores[ligne][colonne][2]
    vivarium_terrain[ligne][colonne][3] += 0.9 * vivarium_herbivores[ligne][colonne][2]
    vivarium_herbivores[ligne][colonne] = [0, 0, 0, 0, 0]
    presence_herbivores.remove([ligne, colonne])

def mort_herbivore_naturelle(k):
    #
    global vivarium_herbivores
    global presence_herbivores
    global vivarium_terrain
    ligne = presence_herbivores[k][0]
    colonne = presence_herbivores[k][1]
    vivarium_terrain[ligne][colonne][3] += int(vivarium_herbivores[ligne][colonne][2])
    vivarium_herbivores[ligne][colonne] = [0, 0, 0, 0, 0]
    del presence_herbivores[k]

## Entretien carnivores ##

def entretien_carnivores():
    global vivarium_carnivores
    global presence_carnivores
    Liste_des_carnivores_a_tuer_a_la_fin_du_cycle = []
    for k in range(len(presence_carnivores)):
        ligne, colonne = presence_carnivores[k][0], presence_carnivores[k][1]
        type = vivarium_carnivores[ligne][colonne][1]
        vivarium_carnivores[ligne][colonne][3] += 1
        for i in range(types_carnivores2[type][9]):

            Cherche_Nour = recherche_nourriture_carnivores(k, type)
            Reussite_chasse = rd.random
            if Cherche_Nour and k not in Liste_des_carnivores_a_tuer_a_la_fin_du_cycle:
                Liste_des_carnivores_a_tuer_a_la_fin_du_cycle += [k]
            elif verification_carnivores(ligne, colonne, type) and not Cherche_Nour:
                mort_par_predation_herbivore(k)
                reproduction_carnivores(ligne, colonne, type)
            elif not verification_carnivores(ligne, colonne,
                                             type) and k not in Liste_des_carnivores_a_tuer_a_la_fin_du_cycle:
                Liste_des_carnivores_a_tuer_a_la_fin_du_cycle += [k]
    Nb_Carv_Tuer = len(Liste_des_carnivores_a_tuer_a_la_fin_du_cycle)
    for k in range(Nb_Carv_Tuer):
        mort_carnivore_naturelle(Nb_Carv_Tuer - 1 - Liste_des_carnivores_a_tuer_a_la_fin_du_cycle[k])

def verification_carnivores(ligne, colonne, type):
    global vivarium_carnivores
    return vivarium_carnivores[ligne][colonne][3] <= types_carnivores2[type][0]

def recherche_nourriture_carnivores(k, type):
    D = []
    global presence_carnivores
    global presence_carnivores
    global presence_herbivores
    global vivarium_carnivores
    global vivarium_herbivores
    LC = presence_carnivores
    LH = presence_herbivores
    Dmin = []
    for herbivores in range(len(LH)):
        ligne, colonne = presence_herbivores[herbivores][0], presence_herbivores[herbivores][1]
        x = abs(LC[k][0] - LH[herbivores][0])
        y = abs(LC[k][1] - LH[herbivores][1])

        if x <= types_carnivores2[type][8] and y <= types_carnivores2[type][8] and vivarium_herbivores[ligne][colonne][
            3] >= 2:
            D += [[(x ** 2 + y ** 2) ** 0.5, LH[herbivores][0], LH[herbivores][1], herbivores]]
    if D == []:
        return True
    Dmin = D[0]
    for i in range(len(D)):
        if math.floor(D[i][0]) <= Dmin[0]:
            Dmin = D[i]
    ligne_ini, colonne_ini = presence_carnivores[k][0], presence_carnivores[k][1]
    presence_carnivores[k][0] = Dmin[1]
    presence_carnivores[k][1] = Dmin[2]
    ligne, colonne = presence_carnivores[k][0], presence_carnivores[k][1]
    vivarium_carnivores[ligne][colonne] = vivarium_carnivores[ligne_ini][colonne_ini]
    vivarium_carnivores[ligne_ini][colonne_ini] = [0, 0, 0, 0, 0]
    return D == []

def nutritition_carnivores(ligne, colonne):
    global presence_carnivores
    global presence_carnivores
    global vivarium_carnivores
    global vivarium_vegetaux
    vivarium_carnivores[ligne][colonne][4] += vivarium_herbivores[ligne][colonne][3]
    vivarium_herbivores[ligne][colonne] = []
    presence_carnivores.remove([ligne, colonne])

def reproduction_carnivores(ligne, colonne, type):
    global vivarium_carnivores
    global presence_carnivores
    maladie = vivarium_carnivores[ligne][colonne][0]
    chance_repro = rd.random()
    if chance_repro <= types_carnivores2[type][2]:
        ligne1 = ligne
        colonne1 = colonne
        ligne1 += rd.randint(-1, 2)
        colonne1 += rd.randint(-1, 2)
        presence_carnivores_truefalse = [ligne1, colonne1] in presence_carnivores
        if 0 <= ligne1 <= taille_vivarium - 1 and 0 <= colonne1 <= taille_vivarium - 1 and presence_carnivores_truefalse == False and verification_eau(
                ligne1, colonne1):
            presence_carnivores += [[ligne1, colonne1]]
            vivarium_carnivores[ligne1][colonne1] = [maladie, type, 0, 0, rd.randint(0, 1)]

def reproduction_carnivores2(ligne, colonne):
    global vivarium_carnivores
    global presence_carnivores
    binome_reproducteur = cherche_partenaire_particuliere(ligne, colonne)
    while binome_reproducteur > 0 and binome_reproducteur < len(presence_carnivores):
        ligne, colonne = rd.randint(0, taille_vivarium - 1), rd.randint(0, taille_vivarium - 1)
        presence_truefalse = [ligne, colonne] in presence_carnivores
        if presence_truefalse == False:
            vivarium_carnivores[ligne][colonne][0] = rd.randint(0, len(maladies_carnivores) - 1)
            vivarium_carnivores[ligne][colonne][1] = rd.randint(0, len(types_carnivores) - 1)
            vivarium_carnivores[ligne][colonne][2] = 0
            vivarium_carnivores[ligne][colonne][3] = 0
            vivarium_carnivores[ligne][colonne][4] = 0
            quota = quota - 1
            presence_carnivores += [[ligne, colonne]]

def cherche_partenaire_particuliere(ligne, colonne):
    global vivarium_carnivores
    global presence_carnivores
    binome_reproducteur = 0
    effectif_efficace = presence_carnivores
    while len(effectif_efficace) >= 1:
        effectif_efficace_proche = []
        for carnivore2 in range(len(effectif_efficace)):
            x = abs(effectif_efficace[0][0] - effectif_efficace[carnivore2][0])
            y = abs(effectif_efficace[0][1] - effectif_efficace[carnivore2][1])
            if x <= types_carnivores2[vivarium_carnivores[ligne][colonne][1]][8] and y <= \
                    types_carnivores2[vivarium_carnivores[ligne][colonne][1]][8] and x != 0 and y != 0:
                effectif_efficace_proche += [presence_carnivores[carnivore2]]
        if effectif_efficace_proche == []:
            del effectif_efficace[0]
        else:
            effectif_efficace_proche = tf(effectif_efficace_proche)
            partenaire_potentiel_trouve = False
            indice_effectif_efficace_proche = 0
            while partenaire_potentiel_trouve == False or indice_effectif_efficace_proche < len(
                    effectif_efficace_proche):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if vivarium_carnivores[effectif_efficace_proche[indice_effectif_efficace_proche][0] + i,
                                               effectif_efficace_proche[indice_effectif_efficace_proche][1] + j] != []:
                            vivarium_carnivores[effectif_efficace_proche[indice_effectif_efficace_proche][0] + i,
                                                effectif_efficace_proche[indice_effectif_efficace_proche][1] + j] = \
                            vivarium_carnivores[effectif_efficace[0][0], effectif_efficace[0][1]]
                            presence_carnivores += [effectif_efficace_proche[indice_effectif_efficace_proche][0] + i,
                                                    effectif_efficace_proche[indice_effectif_efficace_proche][1] + j]
                            presence_carnivores.remove([effectif_efficace[0][0], effectif_efficace[0][1]])
                            binome_reproducteur += 1
                indice_effectif_efficace_proche += 1
            del [efficace_efficace[0]]
    return binome_reproducteur

def mort_carnivore_naturelle(k):
    global vivarium_carnivore
    global presence_carnivores
    global vivarium_terrain
    ligne = presence_carnivores[k][0]
    colonne = presence_carnivores[k][1]
    vivarium_terrain[ligne][colonne][3] += vivarium_carnivores[ligne][colonne][2]
    vivarium_carnivores[ligne][colonne] = [0, 0, 0, 0, 0]
    del [presence_carnivores[k]]

### Cycle principal ###

def cycle_principal():
    # Cette fonction prend en argument le nombre de jour indiquée dans le widget ENTRY et passe le nombre de jours demandés en appelant les fonctions d'entretien
    global vivarium_terrain
    global vivarium_vegetaux
    global presence_vegetaux
    global vivarium_herbivores
    global presence_herbivores
    global vivarium_carnivores
    global presence_carnivores
    global annee_actuelle
    global mois_actuel
    global jour_actuel
    global saison_actuelle
    global nombre_vegetaux
    global nombre_herbivores
    global nombre_carnivores
    global nombre_jours
    global nombre_jours_liste
    jours_a_passer = temps_a_passer()
    t1 = time.time()
    for temps in range(1, jours_a_passer + 1):
        entretien_terrain()
        entretien_vegetaux()
        entretien_herbivores()
        entretien_carnivores()
        jour_actuel += 1
        date()
        nombre_jours += 1
        nombre_jours_liste += [nombre_jours]
        comptage_individus()
    Coord['text'] = '' + str(jour_actuel) + ' ' + str(mois[mois_actuel - 1]) + ' (' + str(
        saisons[saison_actuelle][3]) + ') (année ' + str(annee_actuelle) + ') '
    affichage_terrain()
    affichage_carnivores()
    affichage_vegetaux()
    affichage_herbivores()
    t2 = time.time() - t1
    print(t2)
    return vivarium_vegetaux

def temps_a_passer():
    jours_a_passer = int(entree.get())
    return jours_a_passer

def date():
    # Cette fonction permet d'actualiser la date en fonction des jours passés
    global annee_actuelle
    global mois_actuel
    global jour_actuel
    if jour_actuel == 31:
        mois_actuel += 1
        jour_actuel = 1
    if mois_actuel == 13:
        annee_actuelle += 1
        mois_actuel = 1
    fsaison_actuelle()

def fsaison_actuelle():
    global saison_actuelle
    global mois_actuel
    saison_actuelle = int(mois_actuel / 4)

def comptage_individus():
    # Cette fonction compte chaque jour le nombre d'individus pour le suivi graphique
    global presence_vegetaux
    global presence_herbivores
    global presence_carnivores
    global nombre_vegetaux_liste
    global nombre_herbivores_liste
    global nombre_carnivores_liste
    nombre_vegetaux_liste += [len(presence_vegetaux)]
    nombre_herbivores_liste += [len(presence_herbivores)]
    nombre_carnivores_liste += [len(presence_carnivores)]

### Création du Vivarium ###

global vivarium_terrain
vivarium_terrain = creation_vivarium_terrain(substrats)

global vivarium_carnivores
global presence_carnivores
vivarium_carnivores, presence_carnivores = creation_vivarium_carnivores(taille_vivarium, couleurs_carnivores,
                                                                        maladies_carnivores, nombre_carnivores,
                                                                        types_carnivores)
global vivarium_vegetaux
global presence_vegetaux
vivarium_vegetaux, presence_vegetaux = creation_vivarium_vegetaux(taille_vivarium, couleurs_vegetaux, maladies_vegetaux,
                                                                  nombre_vegetaux, types_vegetaux)
global vivarium_herbivores
global presence_herbivores
vivarium_herbivores, presence_herbivores = creation_vivarium_herbivores(taille_vivarium, couleurs_herbivores,
                                                                        maladies_herbivores, nombre_herbivores,
                                                                        types_herbivores)
comptage_individus()

### INTERFACE GRAPHIQUE ###

## Fenêtre d'information du début ##

selection_liste = ["Sur le plateau il existe 3 types de substrats : \n - le sable en jaune \n - l'argile en marron \n "
                   "- l'eau en bleu \n \n Les petits carrés dans les cases indiquent la présence d'êtres vivants :\n"
                   "- en teintes de vert les végétaux\n- en teintes de violet les herbivores\n"
                   "- en teintes de rouges les carnivores\n\nPour lancer une simulation, veuillez fermer la fenêtre\n"
                   "et entrer un nombre de jour dans le champs de saisi\navant de cliquer sur le bouton pour lancer la simulation."
                   "" , " Vous pourrez observer plusieurs\nmenus déroulant dans la "
                   "fenêtre principale :\n\n=Information= qui vous permet d'obtenir les informations précises\nd'une "
                   "case en choisissant la catégorie qui vous intéresse\n\n=Evolution des effectifs= qui fait "
                   "apparaître\nun graphique permettant de suivre l'évolution\ndes effectifs des différentes catégories "
                   "d'êtres vivants\n\n=Date= permettant de l'afficher\n\n=Editeur de terrain= permettant "
                   "de modifier les substrats\nun par un en cliquand dessus" , "ATTENTION : le passage des jours "
                   "peut être un peu long\ndépendant de l'ordinateur utilisé (de quelques secondes à quelques \nminutes "
                   "pour une dizaine de jours et un ordinateur vraiment vieux)",""]

def selectionner():
    global bottom
    global selection
    selection = listbox.curselection()
    if selection == (0,):
        fenetre_debut_2.forget(bottom)
        bottom = Label(fenetre_debut_2, text=selection_liste[0],bg="#FFFFFF")
        fenetre_debut_2.add(bottom)
    elif selection == (1,):
        fenetre_debut_2.forget(bottom)
        bottom = Label(fenetre_debut_2, text=selection_liste[1],bg="#FFFFFF")
        fenetre_debut_2.add(bottom)
    else:
        fenetre_debut_2.forget(bottom)
        bottom = Label(fenetre_debut_2, text=selection_liste[2],bg="#FFFFFF")
        fenetre_debut_2.add(bottom)

global bottom
global selection
selection=(2,)
fenetre_debut = PanedWindow(height=800,width=800)
fenetre_debut.pack(fill=BOTH,expand=1)
listbox = Listbox(fenetre_debut)
fenetre_debut.add(listbox)
for item in ["Interface","Menus","Avertissements"]:
    listbox.insert(END,item)
fenetre_debut_3 = PanedWindow(fenetre_debut, orient=HORIZONTAL)
fenetre_debut.add(fenetre_debut_3)
afficher_aide = Button(fenetre_debut_3, text="Veuillez selectionner \n une catégorie puis \n appuyez ici pour afficher \n l'aide correspondante",command=selectionner,bg="#48BD0A",bd=4,activebackground="#30770A")
fenetre_debut_3.add(afficher_aide)
fenetre_debut_2 = PanedWindow(fenetre_debut, orient=VERTICAL)
fenetre_debut.add(fenetre_debut_2)
top = Label(fenetre_debut_2, text="Informations",bd=4,bg="#000000",fg="#FFFFFF")
fenetre_debut_2.add(top)
bottom = Label(fenetre_debut_2, text=selection_liste[2],bg="#FFFFFF")
fenetre_debut_2.add(bottom)

## Affichage des quadrillages, des êtres vivants, et de la scrollbar ##

fenetre = Tk()
fenetre.title("Vivarium")
Terrain = Canvas(fenetre, height=taille_vivarium * 30, width=taille_vivarium * 30, scrollregion=(0, 0, taille_vivarium*30,taille_vivarium*30))
Terrain.pack(expand=True,fill=BOTH)
vbar=Scrollbar(fenetre,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=Terrain.yview)
hbar=Scrollbar(fenetre,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=Terrain.xview)
Terrain.config(width=500,height=500)
Terrain.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set)

def affichage_terrain():
    carreau = [[Terrain.create_rectangle(i * 30, j * 30, (i + 1) * 30, (j + 1) * 30, fill="#FFFFFF")
                for i in range(taille_vivarium)] for j in range(taille_vivarium)]

    for ligne in range(taille_vivarium):
        for colonne in range(taille_vivarium):
            if vivarium_terrain[ligne][colonne][0] == 0:
                Terrain.itemconfigure(carreau[ligne][colonne], fill=couleurs_substrats[0])
            elif vivarium_terrain[ligne][colonne][0] == 1:
                Terrain.itemconfigure(carreau[ligne][colonne], fill=couleurs_substrats[1])
            elif vivarium_terrain[ligne][colonne][0] == 2:
                Terrain.itemconfigure(carreau[ligne][colonne], fill=couleurs_substrats[2])

Coord = Label(fenetre)
Coord.pack(pady='10px')

affichage_terrain()

def coloriage_case():
    for ligne in range(taille_vivarium):
        for colonne in range(taille_vivarium):
            if vivarium_terrain[ligne][colonne][1] == 0:
                Terrain.itemconfigure(carreau[ligne][colonne], fill=couleurs_substrats[0])
            else:
                Terrain.itemconfigure(carreau[ligne][colonne], fill=couleurs_substrats[1])

def affichage_vegetaux():
    for k in range(len(presence_vegetaux)):
        ligne, colonne = presence_vegetaux[k][0], presence_vegetaux[k][1]
        closest = Terrain.find_closest(ligne * 30, colonne * 30)
        x1, y1, x2, y2 = Terrain.coords(closest[0])
        id = Terrain.create_rectangle(x1 + 2, y1 + 2, x2 - 15, y2 - 15,
                                      fill=couleurs_vegetaux[vivarium_vegetaux[ligne][colonne][1]])
        if vivarium_vegetaux[ligne][colonne][0] >= 1:
            id = Terrain.create_oval(x1 + 5, y1 + 5, x2 - 18, y2 - 18, fill='ivory')

affichage_vegetaux()

def affichage_carnivores():
    for k in range(len(presence_carnivores)):
        ligne, colonne = presence_carnivores[k][0], presence_carnivores[k][1]
        closest = Terrain.find_closest(ligne * 30, colonne * 30)
        x1, y1, x2, y2 = Terrain.coords(closest[0])
        id = Terrain.create_rectangle(x1 + 15, y1 + 2, x2 - 2, y2 - 15,
                                      fill=couleurs_carnivores[vivarium_carnivores[ligne][colonne][1]])
        if vivarium_carnivores[ligne][colonne][0] >= 1:
            id = Terrain.create_oval(x1 + 18, y1 + 5, x2 - 5, y2 - 18, fill='ivory')

affichage_carnivores()

def affichage_herbivores():
    for k in range(len(presence_herbivores)):
        ligne, colonne = presence_herbivores[k][0], presence_herbivores[k][1]
        closest = Terrain.find_closest(ligne * 30, colonne * 30)
        x1, y1, x2, y2 = Terrain.coords(closest[0])
        id = Terrain.create_rectangle(x1 + 15, y1 + 15, x2 - 2, y2 - 2,
                                      fill=couleurs_herbivores[vivarium_herbivores[ligne][colonne][1]])
        if vivarium_herbivores[ligne][colonne][0] >= 1:
            id = Terrain.create_oval(x1 + 18, y1 + 18, x2 - 5, y2 - 5, fill='ivory')

affichage_herbivores()

## Affichage des menus ##

menuBar = Menu(fenetre)
fenetre['menu'] = menuBar

# Information #

def clic_informations_terrain(event):
    j = event.x // 30
    i = event.y // 30
    eau = vivarium_terrain[i][j][1]
    substrat = substrats[vivarium_terrain[i][j][0]]
    temperature = vivarium_terrain[i][j][2]
    Coord['text'] = 'eau = (' + str(eau) + ') substrat = (' + substrat + ') température = (' + str(temperature) + ')'

def clic_informations_vegetaux(event):
    global presence_vegetaux
    i = event.x // 30
    j = event.y // 30
    presence_vegetaux_truefalse = [i, j] in presence_vegetaux
    if presence_vegetaux_truefalse == False:
        Coord['text'] = 'Pas de vegetaux ici'
    else:
        maladie = maladies_vegetaux[vivarium_vegetaux[i][j][0]]
        vegetal = types_vegetaux[vivarium_vegetaux[i][j][1]]
        age = vivarium_vegetaux[i][j][2]
        Coord['text'] = '(' + vegetal + ') (' + maladie + ') (' + str(age) + ')'

def clic_informations_herbivores(event):
    global presence_herbivores
    i = event.x // 30
    j = event.y // 30
    presence_herbivores_truefalse = [i, j] in presence_herbivores
    if presence_herbivores_truefalse == 0:
        Coord['text'] = 'Pas de herbivores ici'
    else:
        maladie = maladies_herbivores[vivarium_herbivores[i][j][0]]
        herbivore = types_herbivores[vivarium_herbivores[i][j][1]]
        Coord['text'] = '(' + herbivore + ') (' + maladie + ')'

def clic_informations_carnivores(event):
    global presence_carnivores
    i = event.x // 30
    j = event.y // 30
    if presence_carnivores[i][j] == 0:
        Coord['text'] = 'Pas de carnivores ici'
    else:

        maladie = maladies_carnivores[vivarium_carnivores[i][j][0]]
        carnivore = types_carnivores[vivarium_carnivores[i][j][1]]
        Coord['text'] = '(' + carnivore + ') (' + maladie + ')'

def informations_terrain():
    Terrain.bind('<ButtonRelease>', clic_informations_terrain)

def informations_vegetaux():
    Terrain.bind('<ButtonRelease>', clic_informations_vegetaux)

def informations_carnivores():
    Terrain.bind('<ButtonRelease>', clic_informations_carnivores)

def informations_herbivores():
    Terrain.bind('<ButtonRelease>', clic_informations_herbivores)

information_menu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Informations', menu=information_menu)
information_menu.add_command(label='Informations sur le terrain', command=informations_terrain)
information_menu.add_command(label='Informations sur les végétaux', command=informations_vegetaux)
information_menu.add_command(label='Informations sur les herbivores', command=informations_herbivores)
information_menu.add_command(label='Informations sur les carnivores', command=informations_carnivores)

# Evolution des effectifs #

def afficher_effectifs():
    global nombre_vegetaux_liste
    global nombre_herbivores_liste
    global nombre_carnivores_liste
    global nombre_jours_liste
    plt.plot(nombre_jours_liste, nombre_vegetaux_liste, 'green')
    plt.plot(nombre_jours_liste, nombre_herbivores_liste, 'magenta')
    plt.plot(nombre_jours_liste, nombre_carnivores_liste, 'red')
    plt.show()

evolution_des_effectifs_menu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Evolution des effectifs', menu=evolution_des_effectifs_menu)
evolution_des_effectifs_menu.add_command(label='Afficher les graphiques', command=afficher_effectifs)

# Date #

def afficher_date():
    Coord['text'] = '' + str(jour_actuel) + ' ' + str(mois[mois_actuel - 1]) + ' (' + str(
        saisons[saison_actuelle][3]) + ') (année ' + str(annee_actuelle) + ') '

Date_menu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Date', menu=Date_menu)
Date_menu.add_command(label='Afficher la date', command=afficher_date)
afficher_date()

# Editeur #

def clic_edition_substrats(event):
    i = event.x // 30
    j = event.y // 30
    if vivarium_terrain[i][j][0] == 0:
        vivarium_terrain[i][j][0] += 1
    else:
        vivarium_terrain[i][j][0] = 0
    if vivarium_terrain[i][j][0] == 0:
        Terrain.itemconfigure(carreau[i][j], fill=couleurs_substrats[0])
    else:
        Terrain.itemconfigure(carreau[i][j], fill=couleurs_substrats[1])

def edition_substrats():
    Terrain.bind('<ButtonRelease>', clic_edition_substrats)

editeur_de_terrain_menu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Editeur de terrain', menu=editeur_de_terrain_menu)
editeur_de_terrain_menu.add_command(label='Substrats', command=edition_substrats)

# Options #

option_menu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Options', menu=option_menu)
option_menu.add_command(label='Quitter', command=fenetre.destroy)

## Affichage des boutons permettant de passer x jours ##

value = StringVar(fenetre)
value.set("")
entree = Entry(fenetre, textvariable=value, width=25)
Button(fenetre, text='Lancer la simulation', command=cycle_principal, cursor="exchange").pack(side=RIGHT, padx=5,
                                                                                              pady=5)
texteLabel = Label(fenetre, text='Nombre de jours à passer :').pack(side=LEFT, padx=5, pady=5)
entree.pack()

## Affichage de la fenêtre ##

fenetre.mainloop()