# Projet-Python-POO
projet de python avancé sur une application de gestion de stock utilisant la manipulation de base de donne et les interfaces graphiques
Projet Python Avancé - Gestion de Stock avec Tkinter et SQLite

Réalisé par :

· Ahmed Mounir Ahrabar
· Adnane Faiz

Sous la supervision de :

· Pr. M. Hain

Introduction

De nos jours, dans un monde économique où il faut être compétitif et réactif, bien gérer ses stocks est devenu crucial pour les petites et moyennes entreprises. Pourtant, beaucoup continuent de gérer leurs inventaires à la main, avec des papiers ou des tableurs basiques. Cette méthode a ses limites : on fait des erreurs, on ne peut pas suivre les stocks en direct, on perd des infos, et on manque de visibilité sur nos fournisseurs et nos produits.

Pour répondre à ces problèmes, une application de gestion d'inventaire automatisée apparaît comme une solution à la fois économique et efficace. C'est exactement ce que propose ce projet : un système développé en Python, avec une interface simple à utiliser (grâce à Tkinter) et une base de données SQLite intégrée.

L'idée, c'est de permettre aux petites entreprises de gérer l'ensemble de leur cycle de stock, de l'enregistrement des produits et fournisseurs au suivi des commandes. L'objectif ? Centraliser les infos et automatiser les tâches quotidiennes, sans avoir à investir dans des logiciels coûteux.

Au final, ce projet vise à :

· Mieux tracer les produits,
· Faciliter la mise à jour et la consultation des données,
· Garantir une meilleure cohérence et sécurité des informations grâce à la base de données relationnelle.

Analyse de la base de données

1. Modèle conceptuel (MCD)

L'analyse du besoin conduit à l'identification de trois entités principales :

· Produit : représente les articles disponibles en stock.
· Fournisseur : représente les partenaires fournissant les produits.
· Commande : représente les transactions reliant les produits et les fournisseurs.

2. Cardinalités et associations

· Un fournisseur peut fournir plusieurs produits → cardinalité (1, N).
· Un produit peut être fourni par plusieurs fournisseurs → cardinalité (1, N).
· La commande joue ici le rôle d'association entre fournisseur et produit.
· On obtient donc une relation ternaire transformée en table « COMMANDE », comportant deux clés étrangères :
  · idf (clé étrangère vers FOURNISSEUR)
  · idp (clé étrangère vers PRODUIT)

3. Dépendances fonctionnelles

· Pour la table PRODUIT : idp → nomp, prix
· Pour la table FOURNISSEUR : idf → nom, contact
· Pour la table COMMANDE : idc → idf, idp, quantite, datec

Ces dépendances montrent que chaque clé primaire détermine entièrement le reste des attributs.

4. Normalisation

Toutes les tables respectent les trois formes normales (3FN) :

· 1FN : chaque champ contient une valeur atomique.
· 2FN : les dépendances partielles sont éliminées car chaque table possède une clé simple.
· 3FN : aucune dépendance transitive entre attributs non-clés.

5. Implémentation physique

```sql
CREATE TABLE fourn(
  idf INTEGER PRIMARY KEY,
  nom TEXT,
  contact TEXT
);

CREATE TABLE prod(
  idp INTEGER PRIMARY KEY,
  nomp TEXT,
  prix INTEGER
);

CREATE TABLE com(
  idc INTEGER PRIMARY KEY,
  idf INTEGER,
  idp INTEGER,
  quantite INTEGER,
  datec TEXT,
  FOREIGN KEY(idf) REFERENCES fourn(idf),
  FOREIGN KEY(idp) REFERENCES prod(idp)
);
```

Analyse fonctionnelle

L'application offre un ensemble de fonctionnalités principales permettant à l'utilisateur d'interagir facilement avec la base de données.

1. Ajout de données

L'utilisateur peut insérer de nouveaux produits, fournisseurs ou commandes via des champs de saisie dans l'interface. Une vérification est effectuée avant insertion pour éviter les doublons ou les erreurs de saisie.

2. Modification des enregistrements

Les informations existantes (prix, contacts, quantités, etc.) peuvent être mises à jour à tout moment. Une boîte de dialogue confirme le succès de la modification.

3. Suppression d'enregistrements

Il est possible de supprimer un produit, un fournisseur ou une commande en spécifiant l'identifiant correspondant. Une confirmation s'affiche avant la suppression effective.

4. Affichage et consultation

L'utilisateur peut choisir la table à visualiser dans une liste (Produits, Fournisseurs ou Commandes). Les résultats s'affichent dans un tableau interactif (Treeview) permettant un aperçu clair et structuré des données.

5. Interaction fluide

Grâce à l'interface Tkinter, l'utilisateur navigue intuitivement entre les fonctions, sans manipulation de code ni accès direct à la base de données.

Analyse technique

1. Langage et bibliothèques

Le langage utilisé est Python, choisi pour sa simplicité syntaxique, sa richesse en bibliothèques, et sa compatibilité multiplateforme.

Bibliothèques principales :

· sqlite3 : gestion de la base de données embarquée.
· pandas : lecture et manipulation de données SQL sous forme de DataFrame.
· tkinter : création de l'interface graphique.
· ttk et messagebox : widgets améliorés et boîtes de dialogue.

2. Structure du code

Le programme est organisé en plusieurs sections :

· Connexion à la base de données et création des tables.
· Définition des fonctions principales (affiche, insertion, maj, supprimer).
· Création de l'interface Tkinter (fenêtres, labels, champs de saisie, boutons).
· Boucle principale (mainloop) pour le lancement de l'application.

3. Modules et interactions

Les fonctions communiquent directement avec la base de données via des requêtes SQL paramétrées, garantissant la sécurité contre les injections SQL. La fonction affiche() s'appuie sur pandas pour charger et afficher les résultats dans un tableau Tkinter.

Description de l'interface graphique

L'interface est conçue pour être simple, claire et intuitive. Elle se compose de plusieurs éléments principaux :

1. Fenêtre principale

Une fenêtre Tkinter de taille fixe (900x500), avec fond clair et titre « Application de gestion de stock ».

2. Liste de sélection

Une Listbox permet de choisir la table à afficher : Produits, Fournisseurs ou Commandes. Le bouton "Afficher Table" charge les données correspondantes.

3. Zone de saisie

Un ensemble de champs Entry permet d'introduire les informations selon la table choisie (ID, nom, prix, quantité, date...).

4. Tableau d'affichage

Un Treeview de ttk affiche les résultats sous forme tabulaire, avec des en-têtes adaptés à chaque table.

5. Boutons de gestion

Quatre boutons principaux :

· Ajouter (insertion dans la base) - bg="lightgreen"
· Modifier (mise à jour) - bg="khaki"
· Supprimer (suppression d'un enregistrement) - bg="salmon"
· Quitter (fermeture de l'application)

Extrait illustratif :

```python
Button(form_frame, text="Ajouter", command=insertion, bg="lightgreen", width=15)
Button(form_frame, text="Modifier", command=maj, bg="khaki", width=15)
Button(form_frame, text="Supprimer", command=supprimer, bg="salmon", width=15)
```

Fonctionnement de la base de données

La base de données gestion_de_donnes.db contient trois tables liées par des clés étrangères. Chaque opération sur l'interface (ajout, modification, suppression) se traduit par une requête SQL exécutée via cursor.execute().

Étude des cas d'utilisation

1. Cas 1 : Ajout d'un nouveau produit

Un employé saisit un identifiant, un nom et un prix.
→L'application insère les données dans la table prod.
→Un message de succès confirme l'ajout.

2. Cas 2 : Mise à jour d'un fournisseur

L'utilisateur sélectionne Fournisseurs, entre un ID existant et modifie le contact.
→Une requête UPDATE actualise les données.
→Le tableau s'actualise automatiquement.

3. Cas 3 : Création d'une commande

Après avoir ajouté un produit et un fournisseur, l'utilisateur saisit les champs de commande (ID, quantité, date, etc.).
→Une ligne est insérée dans la table com, reliant le produit et le fournisseur.

4. Cas 4 : Consultation des stocks

L'utilisateur choisit Produits dans la liste et clique sur "Afficher Table".
→Le Treeview se remplit instantanément des données issues de SQLite.

Conclusion

Le projet de développement d'une application de gestion d'inventaire en Python répond efficacement aux besoins d'une petite entreprise cherchant à centraliser et automatiser la gestion de ses produits, fournisseurs et commandes.

Grâce à l'association de Python, Tkinter et SQLite, le système offre une solution complète, simple à utiliser et facile à maintenir. L'utilisateur peut ainsi gérer ses stocks en toute autonomie, réduire les erreurs de saisie et gagner un temps considérable dans le suivi des activités quotidiennes.

Au-delà de l'aspect technique, ce projet illustre la capacité de Python à intégrer plusieurs composantes (interface graphique, base de données, manipulation des données) au sein d'une même application cohérente.

Il ouvre enfin la voie à des évolutions plus ambitieuses, telles que l'ajout de statistiques, la gestion des utilisateurs, ou l'intégration dans une architecture web.

En somme, ce travail constitue une base solide pour toute future extension vers une solution de gestion commerciale complète, combinant efficacité, fiabilité et convivialité.
