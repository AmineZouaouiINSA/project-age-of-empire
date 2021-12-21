
import tkinter
import pygame 
from tkinter import *
from tkinter import ttk
import PIL
from PIL import ImageTk
from definitions import *
import main


def fonction_menu_principal() :

    
    fen1=Tk()
    fen1.title("Menu Principal")
    fen1.geometry("1080x800")
    fen1.resizable(width=False,height=False)
  
    graphe=Canvas(fen1, width=1080, height=800,bg="gray")

   
    img = PhotoImage(file="ecran.GIF").zoom(1,1)
    graphe.create_image(500,405, image=img)

    graphe.pack()

    game=Button(fen1, text='Load Save', bg="gray", width=15, height=3, font='arial', command=lambda: fonction_jeu(fen1))
    game.place(x=30, y=50)

    newgame=Button(fen1, text='New Game', bg="gray", width=15, height=3, font='arial', command=lambda: Nouvelpartie(fen1))
    newgame.place(x=30, y=140)

    option=Button(fen1, text='Option', bg="gray", width=15, height=3, font='arial', )
    option.place(x=30, y=620)

    exit=Button(fen1, text='Quit', bg="gray", width=15, height=3, font='arial', command=lambda: fen1.destroy())
    exit.place(x=30, y=710)

    fen1.mainloop()


def Nouvelpartie(fen):

    fen.destroy()
    
    fen2=Tk()
    fen2.title("Setting")
    fen2.geometry("1080x800")
    fen2.resizable(width=False,height=False)
  
    graphe2=Canvas(fen2, width=1080, height=800,bg="white")

    img2 = PhotoImage(file="parametre.GIF").zoom(1,1)
    graphe2.create_image(540,400, image=img2)

    graphe2.pack()



    #Création menu deroulant Taille map
    
    def Mapsize():
        taille = Taille.get()
        print(taille)
        if (taille == "Petit"):
            MAP_SIZE=10
        elif(taille == "Moyen"):
            MAP_SIZE=30
        else:
            MAP_SIZE=40


    Taille = StringVar()
    Taille.set("Petit")

    optionmap = [
        "Petit",
        "Moyen",
        "Grand"
    ]
    graphe2.create_text(715,187,text="Taille de la carte :",font=('Arial',"13"),anchor="n")
    TailleMap=OptionMenu(fen2,Taille,*optionmap)
    TailleMap.place(x=810, y= 180)

    #Création menu déroulant du nombre de population    

    def NombreHabitant():
        nombre = Nombrepop.get()
        print(nombre)

    Nombrepop = StringVar()
    Nombrepop.set("200")

    optionpop = [
        "50",
        "100",
        "200"
    ]
    graphe2.create_text(722,227,text="Nombre d'habitant :",font=('Arial',"13"),anchor="n")
    Nombrepopulation=OptionMenu(fen2,Nombrepop,*optionpop)
    Nombrepopulation.place(x=810, y= 220)

    #Création menu déroulant du nombre de l'age de départ

    def AgeDepart():
        age = AgeDep.get
        print(age)

    AgeDep = StringVar()
    AgeDep.set("Age de pierre")

    option_age_depart = [
        "Age de pierre",
        "Age de l'outil"
    ]

    graphe2.create_text(710,267,text="Age de depart :",font=('Arial',"13"),anchor="n")
    AgeDeDepart=OptionMenu(fen2,AgeDep,*option_age_depart)
    AgeDeDepart.place(x=780, y= 260)




    graphe2.create_text(540,95,text="Jeu standard ",font=('Arial',"15"),anchor="n")

    game=Button(fen2,text='jouer', bg="burlywood4", width=24, height=1, font='arial',command=lambda:fonction_jeu(fen2))
    game.place(x=655, y=710)

    exit=Button(fen2,text='retour', bg="brown3", width=14, height=1, font='arial',command=lambda:fonction_retour(fen2))
    exit.place(x=483, y=630)

    confirmer=Button(fen2,text='confirmer', bg="burlywood4", width=24, height=1, font='arial',command=lambda:Mapsize())
    confirmer.place(x=655, y=670)
    
    fen2.mainloop()


def fonction_jeu(fen):
    fen.destroy()
    main.main()

def fonction_retour(fen) :
    fen.destroy()
    fonction_menu_principal()

fonction_menu_principal()