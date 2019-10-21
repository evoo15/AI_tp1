import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import tp1


def chargerBR():
    print('chargement Base des regles')

    # clears text
    BR_TextField.delete(0, 'end')
    brFile = askopenfilename(initialdir=".",

                             title="Choisir le fichier de la Base des regles",

                             filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))

    BR_TextField.insert(0, brFile)
    print(brFile)


def chargerBF():
    # clears text
    BF_TextField.delete(0, 'end')

    print('chargement Base des faits')
    bfFile = askopenfilename(initialdir=".",

                             title="Choisir le fichier de la Base des faits",

                             filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    BF_TextField.insert(0, bfFile)

    print(bfFile)


def demarrer():
    base = tp1.Base()

    if BF_TextField.get() == '':
        messagebox.showinfo("Information", "Charger la base des faits")
    else:
        base.faitURL = BF_TextField.get()
        if BR_TextField.get() == '':
            messagebox.showinfo("Information", "Charger la base des regles")
        else:
            base.reglesURL = BR_TextField.get()
            base.chargerbase()
            print(mode.get())

            if mode.get() == 0:
                messagebox.showinfo("Information", "Choisir le mode de recherche")

            if mode.get() == 1:
                print('on va saturer')
                tp1.saturerBF(base)
                resultText.config(text=base.trace)
                messagebox.showinfo("SUCCES", "La base des faits est saturée")



            if mode.get() == 2:
                print('on va chercher le but')

                if BUT_TextField.get() == '':
                    messagebox.showinfo("Information", "Saisir le but à chercher")
                else:
                    but = BUT_TextField.get()
                    tp1.chercherBut(but, base)
                    if base.butFound == 1:
                        messagebox.showinfo("SUCCES", "Le but est trouvé ")
                    else:
                        resultText.config(text=base.trace)
                        messagebox.showinfo("ERREUR", "Le but n'est pas trouvé ")



master = tk.Tk()
master.geometry("600x600")

mainFrame = tk.Frame(master)
mainFrame.grid(row=0, column=0, pady=20)
mainLabel = tk.Label(mainFrame,
                     text="                                       TP 1 AI par : Yahya Derbeli - Yassine Ben Ameur ")
mainLabel.grid()

# BOUTON CHARGER BF
chargerBF_Button = tk.Button()
chargerBF_Button["text"] = "Charger BF"
chargerBF_Button["command"] = chargerBF
chargerBF_Button.grid(row=1, column=0, sticky=tk.W
                      )

# BOUTON CHARGER BR
chargerBR_Button = tk.Button()
chargerBR_Button["text"] = "Charger BR"
chargerBR_Button["command"] = chargerBR
chargerBR_Button.grid(row=2, column=0, sticky=tk.W, pady=20
                      )

# TEXT FIELD PATH BF
BF_TextField = tk.Entry(master)
BF_TextField["width"] = 100
BF_TextField.grid(row=1, column=1,
                  sticky=tk.W
                  )

# TEXT FIELD PATH BR
BR_TextField = tk.Entry(master)
BR_TextField["width"] = 100

BR_TextField.grid(row=2, column=1, sticky=tk.W, pady=20
                  )

# VARIABLE FOR TYPE OF SEARCH : saturation/chercher le but
mode = tk.IntVar()

# SATURATION RADIO
tk.Radiobutton(master,
               text="Saturation de la Base des faits",
               variable=mode,
               value=1).grid(row=4, column=0, sticky=tk.W,
                             )
# CHERCHER BUT RADION
radio = tk.Radiobutton(master,
                       text="Chercher un But",
                       variable=mode,
                       value=2).grid(row=5, column=0, sticky=tk.W, pady=20
                                     )

# TEXT FIELD BUT
BUT_TextField = tk.Entry(master)
BUT_TextField["width"] = 50
BUT_TextField.grid(row=5, column=1, sticky=tk.W, pady=20)

tk.Button(master,
          text='Quit',
          command=master.quit).grid(row=6,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(master,
          text='Demarrer', command=demarrer).grid(row=6,
                                                  column=1,
                                                  sticky=tk.W,
                                                  pady=4)

f = tk.Frame(master)
f.grid(row=7)
resultText = tk.Label(f, text="")
resultText.grid(row=7)

tk.mainloop()
