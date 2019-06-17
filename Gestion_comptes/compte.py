# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# Author : Clément Denève
# Function : Gestion of bank account / statistic analysis
# Start : 13/05/2019
# Last update : 27/05/2019
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o

# Importations
import sqlite3
from datetime import datetime
from tkinter import *
import Pmw
import sqlite3
import os

# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o


class Tableur(Frame):
    def __init__(self, fenetre, width, dataset):
        Frame.__init__(self, fenetre,bg='grey') 

        # Attributs
        self.fenetre = fenetre
        self.rows = len(dataset)
        self.columns = width 
        self.dataset = dataset
        self.data = []

        # Affichage
        self.function_display()

    # Functions
    def function_display(self):
        #Placement du cadre principal
        self.grid(row=0,column=0,padx=10,pady=10,sticky='nsew') 

        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.columnconfigure(8, weight=1)
        self.columnconfigure(9, weight=1)
        self.columnconfigure(10, weight=1)

        self.label_total = Label(self, text= 'Montant total : ', bg='lightblue')
        self.label_total.grid(row=2, column=0, columnspan=11, pady=(5, 0), sticky='ns')

        # Création des boutons de commande
        self.label_id = Label(self, text='ID')
        self.label_date = Label(self, text='DATE')
        self.label_datebanque = Label(self, text='DATE RECU')
        self.label_banque = Label(self, text='BANQUE')
        self.label_objet = Label(self, text='OBJET')
        self.label_moyen = Label(self, text='MOYEN DE PAIEMENT')
        self.label_ordre = Label(self, text='ORDRE')
        self.label_montant = Label(self, text='MONTANT')
        self.label_debit = Label(self, text='DEBIT')

        # Placement dans la grille
        self.label_id.grid(row=0, column=2, sticky='nsew')
        self.label_date.grid(row=0, column=3, sticky='nsew')
        self.label_datebanque.grid(row=0, column=4, sticky='nsew')
        self.label_banque.grid(row=0, column=5, sticky='nsew')
        self.label_objet.grid(row=0, column=6, sticky='nsew')
        self.label_moyen.grid(row=0, column=7, sticky='nsew')
        self.label_ordre.grid(row=0, column=8, sticky='nsew')
        self.label_montant.grid(row=0, column=9, sticky='nsew')
        self.label_debit.grid(row=0, column=10, sticky='nsew')
        

        # Création du frame pour le canvas / scrollbar
        self.frame_canvas = Frame(self)
        self.frame_canvas.grid(row=1, column=0, columnspan=11, pady=(5, 0), sticky='ne')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        self.frame_canvas.grid_propagate(False)

        # Création du canevas et lien avec la scrollbar
        self.canvas = Canvas(self.frame_canvas, bg="lightgrey")
        self.canvas.grid(row=0, column=0, sticky="news")
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Création du frame contenant les boutons
        self.frame_buttons = Frame(self.canvas, bg="black")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self.bind_mousewheel)

        # Insertion du jeu de donnée initial
        self.function_loadDataFromDatabase()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        self.frame_buttons.update_idletasks()
        columnWidth = sum([self.data[0][j].winfo_width() for j in range(0, self.columns)])
        rowHeight = self.data[0][0].winfo_height() *33
        self.frame_canvas.config(width=columnWidth + self.vsb.winfo_width(),height=rowHeight)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Affichage du tot
        self.function_updateLabelTotal()
    def function_lineAdd(self):
        self.rows += 1
        line = list()
        for j in range(self.columns): 
            cell = Entry(self.frame_buttons) 
            cell.insert(0, 0) 
            line.append(cell) 
        self.data.insert(0, line)
        self.function_update()
        print("Nombre de lignes actualisé :",self.rows)
    def function_lineRemove(self):
        if self.rows > 0:
            for i in range(self.columns):
                self.data[0][i].destroy()
            del self.data[0]
            self.function_update()
            print("Nombre de lignes actualisé :",self.rows)
    def function_update(self):
        for i in range(len(self.data)):
            self.data[i][0].delete(0)
            self.data[i][0].delete(0)
            self.data[i][0].delete(0)
            self.data[i][0].delete(0)
            self.data[i][0].insert(0, i+1)
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                self.data[i][j].grid(row=i+1, column=j)
        self.rows = len(self.data)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.function_updateLabelTotal()
    def function_insertData(self, dataset):
        for i in range(len(dataset)):
            self.function_lineAdd()

        for i in range(len(dataset)):
            Transaction_input.adds += 1
            for j in range(len(dataset[0])):
                self.data[i][j].delete(0, last=None)
                self.data[i][j].insert(0, dataset[i][j])
                if j==8:
                    print(self.data[i][j].get())
                    if self.data[i][j].get() == '0':
                        self.data[i][j]['bg'] = 'red'
                        self.data[i][j-1]['bg'] = 'red'
                    if self.data[i][j].get() == '1':
                        self.data[i][j]['bg'] = 'lightgreen'
                        self.data[i][j-1]['bg'] = 'lightgreen'

        for i in range(len(self.data)):
            self.data[i][0].delete(0)
            self.data[i][0].delete(0)
            self.data[i][0].delete(0)
            self.data[i][0].delete(0)
            self.data[i][0].insert(0, i+1)
    def function_removeData(self):
        while self.rows > 0:
            for i in range(self.columns):
                self.data[0][i].destroy()
            del self.data[0]
            self.function_update()
            print("Nombre de lignes actualisé :",self.rows)
    def function_saveToDatabase(self,lines=0):
        self.function_getRawData()

        #Connection
        conn =sqlite3.connect(os.getcwd()+"/data/comptes.db") 
        cur =conn.cursor()

        for i in range(Transaction_input.adds):
            donnee = (self.donneesBrutes[i][1:])
            print(donnee)

            #Insertion
            cur.execute("INSERT INTO transactions(date_emission,date_recu,banque,objet,moyen_paiement,ordre,montant,credit) VALUES(?,?,?,?,?,?,?,?)", donnee)
            #Fermeture des connections
            conn.commit()
            Transaction_input.adds -= 1
        cur.close()
        conn.close()
    def function_getRawData(self):
        self.donneesBrutes =  []

        for i in range(len(self.data)):
            line = []
            for j in range(len(self.data[0])):
                line.append(self.data[i][j].get())
            self.donneesBrutes.append(line)


        for i in range(len(self.donneesBrutes)):
            self.donneesBrutes[i][0] = float(self.donneesBrutes[i][0])
            self.donneesBrutes[i][7] = float(self.donneesBrutes[i][7])
            self.donneesBrutes[i][8] = float(self.donneesBrutes[i][8])
        print(self.donneesBrutes)
    def function_loadDataFromDatabase(self):
        #Connection
        conn =sqlite3.connect(os.getcwd()+"/data/comptes.db") 
        cur =conn.cursor()

        #Insertion
        cur.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 33")
        self.dataset = []
        for i in cur:
            self.dataset.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]])
        print(self.dataset)
        self.function_insertData(self.dataset)
        Transaction_input.adds -= len(self.dataset)

        #Fermeture des connections
        conn.commit()
        cur.close()
        conn.close()
    def function_updateLabelTotal(self):
        somme = 0
        for i in range(len(self.data)):
            somme += round(float(self.data[i][7].get()))
        self.label_total['text'] = "Montant total : " + str(somme)
    # Binds
    def bind_mousewheel(self, event):

        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")



# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o


class Transaction_input(Frame):
    adds = 0
    def __init__(self, table, fenetre):
        # Initialisation du cadre
        Frame.__init__(self, fenetre,bg='lightblue', height = 150) 

        # Attributs
        self.moyen = ['Carte bancaire','Espèces', 'Virement', 'Chèque', 'Autre']
        self.banques = ['La Banque Postale', 'Boursorama', 'Crédit mutuel']
        self.objet = ['Nourriture', 'Transport', 'Loisirs', 'Travail', 'Vêtements']
        self.table = table
        self.credit = True

        # Fonctions utilitaires
        self.function_display()

    def function_dateOfToday(self):
        date = datetime.now()

        if len(str(date.day)) == 1:
            jour = '0'+str(date.day)
        else:
            jour = str(date.day)

        if len(str(date.month)) == 1:
            mois = '0'+str(date.month)
        else:
            mois = str(date.month)
        self.date_emission = "{}/{}/{}".format(jour,mois,str(date.year))
    def function_display(self):
        # Initialisation et config du frame
        self.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)

        self.button_valider = Button(self, text='Valider la saisie', command=self.function_confirmSelection)
        self.button_valider.grid(row=2, column = 6, sticky='nsew')
        self.button_valider = Button(self, text='Enregistrer les données', command=self.function_saveData)
        self.button_valider.grid(row=2, column = 5, sticky='nsew')
        self.button_valider = Button(self, text='Supprimer dernière saisie', command=self.function_deleteLastLine)
        self.button_valider.grid(row=2, column = 4, sticky='nsew')
        self.button_valider = Button(self, text='Charger données database', command=self.function_loadData)
        self.button_valider.grid(row=2, column = 3, sticky='nsew')

        # Calcul de la date
        self.function_dateOfToday()

        # Configuration des colonnes
        for i in range(7):
            self.columnconfigure(i, weight=1)

        # Affichage des Entrées
        self.entry_dateRecu = Entry(self, text="Saisir la date du recu", justify='center')
        self.entry_dateRecu.insert(0, self.date_emission)
        self.combo_banque = Pmw.ComboBox(self, labelpos = NW,
                             label_text = 'Choisir la banque',
                             scrolledlist_items = self.banques,
                             listheight = 150
                             )
        self.combo_objet = Pmw.ComboBox(self, labelpos = NW,
                             label_text = 'Choisir la catégorie',
                             scrolledlist_items = self.objet,
                             listheight = 150
                             )
        self.combo_moyenPaiement = Pmw.ComboBox(self, labelpos = NW,
                             label_text = 'Choisissez le moyen',
                             scrolledlist_items = self.moyen,
                             listheight = 150
                             )
        self.entry_ordre = Entry(self, text="Saisir l'ordre")
        self.entry_montant = Entry(self, text="Saisir le montant")
        self.checkbutton_debit = Checkbutton(self, bg='lightgreen', command=self.function_checkbuttonColor)
        self.Label_dateRecu = Label(self, text="Saisir la date du recu")
        self.Label_ordre = Label(self, text="Saisir l'ordre")
        self.Label_montant = Label(self, text="Saisir le montant")
        self.Label_debit = Label(self, text="Débit / Crédit")

        # Valeurs initiales
        self.combo_banque.selectitem(0)
        self.combo_moyenPaiement.selectitem(0)
        self.checkbutton_debit.select()

        # Placement dans la grille
        self.entry_dateRecu.grid(row=1, column=0, sticky='nsew')
        self.combo_banque.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.combo_objet.grid(row=0, column=2, rowspan=2, sticky='nsew')
        self.combo_moyenPaiement.grid(row=0, column=3, rowspan=2, sticky='nsew')
        self.entry_ordre.grid(row=1, column=4, sticky='nsew')
        self.entry_montant.grid(row=1, column=5, sticky='nsew')
        self.checkbutton_debit.grid(row=1, column=6, sticky='nsew')
        self.Label_dateRecu.grid(row=0, column=0, sticky='nsew')
        self.Label_ordre.grid(row=0, column=4, sticky='nsew')
        self.Label_montant.grid(row=0, column=5, sticky='nsew')
        self.Label_debit.grid(row=0, column=6, sticky='nsew')
    def function_checkbuttonColor(self):
        if self.checkbutton_debit['bg'] == 'red':
            self.checkbutton_debit['bg'] = 'lightgreen'
            self.credit = True

        else:
            self.checkbutton_debit['bg'] = 'red'
            self.credit = False
    def function_confirmSelection(self):
        donnees, tab = [], []
        donnees.append(self.table.rows +1)
        donnees.append(self.date_emission)
        donnees.append(self.entry_dateRecu.get())
        donnees.append(self.combo_banque.get())
        donnees.append(self.combo_objet.get())
        donnees.append(self.combo_moyenPaiement.get())
        donnees.append(self.entry_ordre.get())
        if self.credit == True:
            try:
                donnees.append(float(self.entry_montant.get()))
            except:
                donnees.append(0)
        else:
            try:
                donnees.append(-float(self.entry_montant.get()))
            except:
                donnees.append(0)
        donnees.append(self.credit)
        tab.append(donnees)

        self.table.function_insertData(tab)
        print(donnees)
    def function_saveData(self):

        self.table.function_saveToDatabase(Transaction_input.adds)
    def function_deleteLastLine(self):

        self.table.function_lineRemove()
    def function_loadData(self):

        self.table.function_loadDataFromDatabase()


# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o


class Application():
    def __init__(self, master):
        self.master = master
        self.function_display()
        dataset = [[1, '27/05/2019', '30/05/2019', 'La Banque Postale', 'VETEMENT', 'Carte Bancaire','CELIOCLUB', -69.99, False],
               [2, '27/05/2019', '31/05/2019', 'La Banque Postale', 'VETEMENT', 'Espèce','CELIOCLUB', -199.99, False],
               [3, '27/05/2019', '01/06/2019', 'Credit Agricole', 'Transport', 'Carte Bancaire','LUFTHANSA', -69.99, False],
               [4, '27/05/2019', '01/06/2019', 'Boursorama', 'Pension', 'Virement','GOUV', 437, True],
               ]
        Transaction_input.adds = 0
        self.table = Tableur(self.frame_center, 9, dataset)
        self.input = Transaction_input(self.table, self.frame_up)

    def function_display(self):
        # Configuration de la fenêtre
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Définition frame global
        self.frame_main = Frame(self.master, bg = 'cyan')
        self.frame_main.grid(row=0, column=0, sticky='nsew')
        self.frame_main.rowconfigure(0, weight=1)
        self.frame_main.rowconfigure(1, weight=6)
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.columnconfigure(1, weight=5)

        # Définition sous parties
        self.frame_up = Frame(self.frame_main, height=150,bg='lightblue')
        self.frame_left = Frame(self.frame_main, width=400 ,bg='orange')
        self.frame_center = Frame(self.frame_main, bg='black')

        # Remplissage de la grille
        self.frame_up.grid(row=0, column=1,sticky='nsew')
        self.frame_left.grid(row=1, column=0, sticky='nsew')
        self.frame_center.grid(row=1, column=1, sticky='nsew')
        self.frame_up.rowconfigure(0, weight=1)
        self.frame_up.columnconfigure(0, weight=1)
        self.frame_center.rowconfigure(0, weight=1)
        self.frame_center.columnconfigure(0, weight=1)


# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o


def main():
    root = Pmw.initialise()
    root.title("Gestion de Comptes")
    root.wm_state('zoomed')
    Application(root)
    root.mainloop()
if __name__ == "__main__":
    main()

 