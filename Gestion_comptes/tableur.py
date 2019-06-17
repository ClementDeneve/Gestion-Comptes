# Tableur python
from tkinter import *

class Tableur(Frame):
    def __init__(self, fenetre, width, dataset):
        Frame.__init__(self, fenetre,bg='grey') 
        self.fenetre = fenetre
        self.rows = len(dataset)
        self.columns = width 
        self.dataset = dataset
        self.grid(row=0,column=0,padx=10,pady=10,sticky='nsew') 
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        # Boutons de commande
        self.button_add = Button(self, text='Enlever une ligne', command=self.remove_line)
        self.button_add.grid(row=0, column=0, sticky='nsew')
        self.button_add = Button(self, text='Ajouter une ligne', command=self.add_line)
        self.button_add.grid(row=0, column=1, sticky='nsew')


        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = Frame(self)
        self.frame_canvas.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky='ne')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, bg="lightgrey")
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Create a frame to contain the buttons
        self.frame_buttons = Frame(self.canvas, bg="black")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
        self.data = []

        self.canvas.bind_all("<MouseWheel>", self.bind_mousewheel)

        self.insert_data(self.dataset)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        columnWidth = sum([self.data[0][j].winfo_width() for j in range(0, self.columns)])
        rowHeight = self.data[0][0].winfo_height() *33
        self.frame_canvas.config(width=columnWidth + self.vsb.winfo_width(),height=rowHeight)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def bind_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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

    def insert_data(self, dataset):
        for i in range(len(dataset)):
            self.add_line()
        for i in range(len(dataset)):
            for j in range(len(dataset[0])):
                self.data[i][j].delete(0, last=None)
                self.data[i][j].insert(0, dataset[i][j])

    def remove_data(self):
        while self.rows > 0:
            for i in range(self.columns):
                self.data[0][i].destroy()
            del self.data[0]
            self.update()
            print("Nombre de lignes actualisé :",self.rows)




  





fenetre = Tk() 
frame = Frame(fenetre)
frame.grid(sticky='nsew')
donnees = [[1, '27/05/2019', '30/05/2019', 'La Banque Postale', 'VETEMENT', 'Carte Bancaire','CELIOCLUB', 69.99, True],
               [2, '27/05/2019', '31/05/2019', 'La Banque Postale', 'VETEMENT', 'Espèce','CELIOCLUB', 199.99, True],
               [3, '27/05/2019', '01/06/2019', 'Credit Agricole', 'Transport', 'Carte Bancaire','LUFTHANSA', 69.99, True],
               [4, '27/05/2019', '01/06/2019', 'Boursorama', 'Pension', 'Virement','GOUV', 437, False],
               ]
interface = Tableur(frame, 9, donnees) 

interface.mainloop()