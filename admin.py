from tkinter import *
import tkinter
import cx_Oracle
import tkinter.ttk as ttk

utilizator = 'c##cristina'
parola = 'crisw8'

class Aplicatie(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        connection = cx_Oracle.connect(utilizator, parola, "localhost:1522/orcl", encoding="UTF-8")
        cursor = connection.cursor()
        comenzi = ""
        rezultat = cursor.execute("SELECT u.nume || ' a comandat ' || c.cantitate || ' bucati de ' || p.nume || ' cu livrare la urmatoarea adresa: ' || c.adresa_de_livrare || ' in data de ' || c.data_comanda || '\n' FROM comenzi c, produse p, utilizator u WHERE c.id_produs=p.id_produs AND c.id_utilizator=u.id_utilizator ORDER BY c.data_comanda").fetchall()
        for comanda in rezultat:
            comenzi += comanda[0]
            comenzi += "\n"
        Label(self, text=comenzi).pack()
        self.pack()
        connection.close()

root = Tk()
app = Aplicatie(master=root)
app.mainloop()
