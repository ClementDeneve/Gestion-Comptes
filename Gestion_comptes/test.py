# Importations
from tkinter import *

# Fenetre principale
root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


class Tableur(Frame):
    def __init__(self, fenetre, height, width):
        Frame.__init__(self, fenetre,bg='grey') 
        self.fenetre = fenetre
        self.rows = height
        self.columns = width 
        self.grid(row=0,column=0,sticky='nsew') 


        # Boutons de commande
        self.button_add = Button(self, text='Enlever une ligne', command=self.remove_line)
        self.button_add.grid(row=0, column=0, sticky='nsew')
        self.button_add = Button(self, text='Ajouter une ligne', command=self.add_line)
        self.button_add.grid(row=0, column=1, sticky='nsew')


        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = Frame(self)
        self.frame_canvas.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, bg="yellow")
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Create a frame to contain the buttons
        self.frame_buttons = Frame(self.canvas, bg="blue")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
        self.data = []

        for i in range(0, self.rows):
            line=[]
            for j in range(0, self.columns):
                line.append(Entry(self.frame_buttons))
                line[j].insert(0, 0)
                line[j].grid(row=i, column=j, sticky='news')
            self.data.append(line)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum([self.data[0][j].winfo_width() for j in range(0, self.columns)])
        first5rows_height = sum([self.data[i][0].winfo_height() *20])
        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                            height=first5rows_height)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_line(self):
        self.rows += 1
        line = list()
        for j in range(self.columns): 
            cell = Entry(self.frame_buttons) 
            cell.insert(0, 0) 
            line.append(cell) 
        self.data.insert(0, line)
        self.update()
        print("Nombre de lignes actualisé :",self.rows)


    def remove_line(self):
        if self.rows > 0:
            for i in range(self.columns):
                self.data[0][i].destroy()
            del self.data[0]
            self.update()
            print("Nombre de lignes actualisé :",self.rows)

    def update(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                self.data[i][j].grid(row=i+1, column=j)
        self.rows = len(self.data)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


import Pmw          
def changeCoul(col):
     fen.configure(background = col)
def changeLabel():
    lab.configure(text = combo.get())
couleurs = ('navy', 'royal blue', 'steelblue1', 'cadet blue',
           'lawn green', 'forest green', 'dark red',
           'grey80','grey60', 'grey40', 'grey20')
   
fen = Pmw.initialise()
bou = Button(fen, text ="Test", command =changeLabel)
bou.grid(row =1, column =0, padx =8, pady =6)
lab = Label(fen, text ='néant', bg ='ivory')
lab.grid(row =1, column =1, padx =8)

combo = Pmw.ComboBox(fen, labelpos = NW,
                     label_text = 'Choisissez la couleur :',
                     scrolledlist_items = couleurs,
                     listheight = 150,
                     selectioncommand = changeCoul)
combo.grid(row =2, columnspan =2, padx =10, pady =10)

fen.mainloop()