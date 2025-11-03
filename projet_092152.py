#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Converted from Jupyter Notebook: notebook.ipynb
Conversion Date: 2025-11-03T20:26:35.788Z
"""

import sqlite3
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox

db = sqlite3.connect("gestion_de_donnes.db")
cursor = db.cursor()
# Creation des tables
cursor.execute("CREATE TABLE IF NOT EXISTS fourn(idf INTEGER PRIMARY KEY,nom TEXT,contact TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS prod(idp INTEGER PRIMARY KEY,nomp TEXT,prix INTEGER);")
cursor.execute("CREATE TABLE IF NOT EXISTS com(idc INTEGER PRIMARY KEY,idf INTEGER,idp INTEGER,quantite INTEGER,datec TEXT,FOREIGN KEY(idf) REFERENCES fourn(idf),FOREIGN KEY(idp) REFERENCES prod(idp));")
db.commit()

def affiche(table):
    for item in tree.get_children():
        tree.delete(item)
    try:
        df = pd.read_sql(f"SELECT * FROM {table}", db)
        for row in df.values.tolist():
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Erreur", f"Affichage impossible : {e}")

def insertion():
    table = liste.get(ACTIVE)
    try:
        if table == "Produits":
            idp = int(entry1.get())
            nomp = entry2.get()
            prix = int(entry3.get())
            cursor.execute("INSERT OR IGNORE INTO prod VALUES (?, ?, ?)", (idp, nomp, prix))
        elif table == "Fournisseurs":
            idf = int(entry1.get())
            nom = entry2.get()
            contact = entry3.get()
            cursor.execute("INSERT OR IGNORE INTO fourn VALUES (?, ?, ?)", (idf, nom, contact))
        elif table == "Commandes":
            idc = int(entry1.get())
            idf = int(entry2.get())
            idp = int(entry3.get())
            qte = int(entry4.get())
            datec = entry5.get()
            cursor.execute("INSERT OR IGNORE INTO com VALUES (?, ?, ?, ?, ?)", (idc, idf, idp, qte, datec))
        else:
            messagebox.showwarning("Erreur", "Aucune table sélectionnée !")
            return
        db.commit()
        messagebox.showinfo("Succès", "Insertion réussie")
        affiche_table()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer():
    table = liste.get(ACTIVE)
    try:
        id_val = int(entry1.get())
        if table == "Produits":
            cursor.execute("DELETE FROM prod WHERE idp=?", (id_val,))
        elif table == "Fournisseurs":
            cursor.execute("DELETE FROM fourn WHERE idf=?", (id_val,))
        elif table == "Commandes":
            cursor.execute("DELETE FROM com WHERE idc=?", (id_val,))
        db.commit()
        messagebox.showinfo("Succès", "Suppression réussie ")
        affiche_table()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def maj():
    table = liste.get(ACTIVE)
    try:
        if table == "Produits":
            idp = int(entry1.get())
            nomp = entry2.get()
            prix = int(entry3.get())
            cursor.execute("UPDATE prod SET nomp=?, prix=? WHERE idp=?", (nomp, prix, idp))
        elif table == "Fournisseurs":
            idf = int(entry1.get())
            nom = entry2.get()
            contact = entry3.get()
            cursor.execute("UPDATE fourn SET nom=?, contact=? WHERE idf=?", (nom, contact, idf))
        elif table == "Commandes":
            idc = int(entry1.get())
            qte = int(entry4.get())
            datec = entry5.get()
            cursor.execute("UPDATE com SET quantite=?, datec=? WHERE idc=?", (qte, datec, idc))
        db.commit()
        messagebox.showinfo("Succes", "Mise a jour reussie")
        affiche_table()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def affiche_table():
    choix = liste.get(ACTIVE)
    if choix == "Produits":
        tree.config(columns=("idp", "nomp", "prix"))
        tree.heading("idp", text="ID Produit")
        tree.heading("nomp", text="Nom Produit")
        tree.heading("prix", text="Prix")
        affiche("prod")
    elif choix == "Fournisseurs":
        tree.config(columns=("idf", "nom", "contact"))
        tree.heading("idf", text="ID Fournisseur")
        tree.heading("nom", text="Nom")
        tree.heading("contact", text="Contact")
        affiche("fourn")
    elif choix == "Commandes":
        tree.config(columns=("idc", "idf", "idp", "quantite", "datec"))
        tree.heading("idc", text="ID Commande")
        tree.heading("idf", text="ID Fourn")
        tree.heading("idp", text="ID Prod")
        tree.heading("quantite", text="Quantité")
        tree.heading("datec", text="Date")
        affiche("com")
    else:
#Tkinter-----------------------------------------------------------------------------------
messagebox.showinfo("Info", "Choisissez une table à afficher.")
window = Tk()
window.title("Application de gestion de stock")
window.geometry("900x500")
window.configure(bg="#f3f3f3")

frame = Frame(window, bg="#f3f3f3")
frame.pack(padx=10, pady=10)

# Listbox and Afficher button spanning two columns
Label(frame, text="Choisissez une table :", bg="#f3f3f3", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
liste = Listbox(frame, height=4, width=40)
liste.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nw")
liste.insert(1, "Produits")
liste.insert(2, "Fournisseurs")
liste.insert(3, "Commandes")

Button(frame, text="Afficher Table", command=affiche_table, bg="#add8e6", width=40).grid(row=2, column=0, columnspan=2, pady=5)

tree = ttk.Treeview(frame, columns=("1", "2", "3"), show="headings", height=15)
tree.grid(row=3, column=0, rowspan=6, padx=10, pady=10)

form_frame = Frame(frame, bg="#f3f3f3")
form_frame.grid(row=3, column=1, sticky="n", padx=10)

Label(form_frame, text="Champ 1 (ID):", bg="#f3f3f3").grid(row=0, column=0)
entry1 = Entry(form_frame, width=20)
entry1.grid(row=0, column=1)

Label(form_frame, text="Champ 2:", bg="#f3f3f3").grid(row=1, column=0)
entry2 = Entry(form_frame, width=20)
entry2.grid(row=1, column=1)

Label(form_frame, text="Champ 3:", bg="#f3f3f3").grid(row=2, column=0)
entry3 = Entry(form_frame, width=20)
entry3.grid(row=2, column=1)

Label(form_frame, text="Champ 4:", bg="#f3f3f3").grid(row=3, column=0)
entry4 = Entry(form_frame, width=20)
entry4.grid(row=3, column=1)

Label(form_frame, text="Champ 5:", bg="#f3f3f3").grid(row=4, column=0)
entry5 = Entry(form_frame, width=20)
entry5.grid(row=4, column=1)

Button(form_frame, text="Ajouter", command=insertion, bg="lightgreen", width=15).grid(row=5, column=0, pady=5)
Button(form_frame, text="Modifier", command=maj, bg="khaki", width=15).grid(row=5, column=1, pady=5)
Button(form_frame, text="Supprimer", command=supprimer, bg="salmon", width=15).grid(row=6, column=0, pady=5)
Button(form_frame, text="Quitter", command=window.destroy, bg="#000", fg="#fff", width=15).grid(row=6, column=1, pady=5)

window.mainloop()
db.close()