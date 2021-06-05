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
        Label(self, text="User:").pack()
        self.username = Text(self, height=1, width=20)
        self.username.pack()
        self.login = Button(self, text="Log in", command=self.login_app)
        self.login.pack()

    def login_app(self):
        connection = cx_Oracle.connect(utilizator, parola, "localhost:1522/orcl", encoding="UTF-8")
        cursor = connection.cursor()
        login = cursor.execute("SELECT id_utilizator FROM utilizator WHERE nume=:1", (self.username.get(1.0, END).replace("\n", ""),))
        user_id = login.fetchall()
        if len(user_id) == 0:
            Label(self, text="Utilizator inexistent!").pack()
        else:
            self.user_id = user_id[0][0]
            self.draw_application()
        connection.close()

    def draw_application(self):
        for child in self.winfo_children():
            child.destroy()
        Label(self, text="Selecteaza cantitatea inainte de a cumpara:").pack()
        self.cantitate = Spinbox(self, from_=1, to=10)
        self.cantitate.pack()
        Label(self, text="Introduceti adresa de livrare:").pack()
        self.adresa = Text(self, height=1, width=50)
        self.adresa.pack()
        connection = cx_Oracle.connect(utilizator, parola, "localhost:1522/orcl", encoding="UTF-8")
        cursor = connection.cursor()
        produse = cursor.execute("SELECT p.nume, dp.pret, dp.stoc_disponibil FROM produse p, detalii_produse dp WHERE p.id_produs=dp.id_produs and stoc_disponibil>0").fetchall()
        for produs in produse:
            nume = produs[0]
            pret = produs[1]
            stoc = produs[2]
            denumire = nume + " la pretul de " + str(pret) + " lei. Grabeste-te! Au mai ramas doar " + str(stoc) + " produse."
            Label(self, text=denumire).pack()
            Button(self, text="Cumpara", command=(lambda nume: lambda: self.cumpara(nume))(nume)).pack()
        comenzi = ""
        rezultat = cursor.execute("SELECT u.nume || ' a comandat ' || c.cantitate || ' bucati de ' || p.nume || ' cu livrare la urmatoarea adresa: ' || c.adresa_de_livrare FROM comenzi c, produse p, utilizator u WHERE c.id_produs=p.id_produs AND c.id_utilizator=u.id_utilizator AND u.id_utilizator=" + str(self.user_id)).fetchall()
        for comanda in rezultat:
            comenzi += comanda[0]
            comenzi += "\n"
        Label(self, text=comenzi).pack()
        self.pack()
        connection.close()

    def cumpara(self, nume_produs):
        cantitate = int(self.cantitate.get())
        connection = cx_Oracle.connect(utilizator, parola, "localhost:1522/orcl", encoding="UTF-8")
        cursor = connection.cursor()
        stoc = cursor.execute("SELECT p.id_produs, dp.stoc_disponibil FROM produse p, detalii_produse dp WHERE p.id_produs=dp.id_produs AND p.nume=:1", (nume_produs, )).fetchone()
        id_produs = stoc[0]
        stoc_produs = stoc[1]
        if cantitate > stoc_produs:
            Label(self, text="Nu se poate! Nu mai sunt produse pe stoc. Reveniti, stocul se va reface curand!").pack()
        else:
            cursor.execute("UPDATE detalii_produse SET stoc_disponibil=stoc_disponibil-" + str(cantitate) + " WHERE id_produs=" + str(id_produs))
            cursor.execute("INSERT INTO comenzi(id_utilizator, id_produs, cantitate, adresa_de_livrare, data_comanda) VALUES (:1, :2, :3, :4, SYSDATE)", (self.user_id, id_produs, cantitate, self.adresa.get(1.0, END).replace("\n", "")))
            connection.commit()
        connection.close()
        self.draw_application()

root = Tk()
app = Aplicatie(master=root)
app.mainloop()