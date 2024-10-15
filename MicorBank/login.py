from tkinter import *
import tkinter as tk
import sqlite3
import time
from tkinter import messagebox
from PIL import Image, ImageTk
#import main


### Funkcje --------------------------- ###
def btn_clicked(): 
    logowanie("admin","password")     

### ----------------------------------- ###
def logowanie(log, pas):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    zapytanie = f"SELECT * FROM customer WHERE login = '{log}'  AND password = '{pas}';"
    c.execute(zapytanie)
    data = c.fetchall()

    if not data:
        messagebox.showinfo("UWAGA", "Brak takiego uzytkownika w bazie,\n lub blednie podane haslo.\nSprobuj raz jeszcze!")
    else:
            


        window.destroy()
        main(data[0])
        #main_windows
        return data[0]


### Main Form --------------------------- ###


### Main Frame ------------------------ ###
window = Tk()
window.title('Aplikacja Micro Bank - Logowanie')

width = 1000 # Width 
height = 600 # Height

screen_width = window.winfo_screenwidth()  # Width of the screen
screen_height = window.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
 
window.geometry('%dx%d+%d+%d' % (width, height, x, y))

#window.geometry("1000x600")
#window.eval('tk::PlaceWindow . center')
window.configure(bg = "#ffffff")

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"img/background.png")
background = canvas.create_image(
    502, 300,
    image=background_img)

img0 = PhotoImage(file = f"img/img0.png")

password = tk.StringVar()

entry0_img = PhotoImage(file = f"img/img_textBox0.png")
entry0_bg = canvas.create_image(
    500.0, 250.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#343f54", 
    foreground="white",
    insertbackground="white",
    font=('Georgia 14'),
    highlightthickness = 0)

entry0.place(
    x = 362.0, y = 226, 
    width = 272.0,
    height = 48)

entry1_img = PhotoImage(file = f"img/img_textBox1.png")
entry1_bg = canvas.create_image(
    500.0, 350.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#343f54", 
    foreground="white",
    insertbackground="white",
    font=('Georgia 14'),
    textvariable=password, show="*",
    highlightthickness = 0)

entry1.place(
    x = 362.0, y = 326,
    width = 272.0,
    height = 48)

b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 430, y = 450,
    width = 140,
    height = 36)


### ----------------------------------- ###

def main(data):
    main = tk.Tk()
    main.title('Micro Bank - Panel główny')

    main.resizable(False, False)

    width = 1400 # Width 
    height = 750 # Height

    screen_width = main.winfo_screenwidth()  # Width of the screen
    screen_height = main.winfo_screenheight() # Height of the screen
    
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    
    main.geometry('%dx%d+%d+%d' % (width, height, x, y))
    main.configure(bg = "white")

    ### Logo Frame ---------------- ### ------------------------------------------------------------------------- ###
    LogoFrame=Frame(main,width=1400,height=100)
    LogoFrame.grid(row=0, column=0, sticky=NSEW)
    LogoFrame.configure(bg = "white")


    LogoFrame_1=Frame(LogoFrame, width=300, height=100, bg="white")
    LogoFrame_2=Frame(LogoFrame, width=956, height=100, bg="white")
    LogoFrame_3=Frame(LogoFrame, width=200, height=100, bg="white")

    LogoFrame_1.grid(row=0, column=0, sticky=NSEW)
    LogoFrame_2.grid(row=0, column=1, sticky=NSEW)
    LogoFrame_3.grid(row=0, column=2, sticky=NSEW)


    ## - Logo Label --- ##
    img_logo = PhotoImage(name="logo", file="img/img_logo.png")
    label_logo = Label(LogoFrame_1, image=img_logo, bd=0)
    label_logo.grid(padx=(15,0))  
    label_logo.configure(bg="white", width=200, anchor=W)
    ## - Koniec Logo Label --- ##    

    ## - Lable Info --- ##
    label_string = StringVar()
    label_string.set("Witaj, "+data[2] + " " + data[3])
    label_info = Label(LogoFrame_2, textvariable=label_string, bg="white", fg="#2B2B43", font=('Georgia 14'))
    #label_info.grid(row=0, column=0, rowspan=2, pady=(0,0), padx=(0,450), sticky=W)
    label_info.place(x=10,y=10)
        
    Linia1_string = StringVar()
    Linia2_string = StringVar()
    Linia3_string = StringVar()
    Linia4_string = StringVar()

    dane1 = (f'{data[5]:,}'.replace(',', ' '))
    dane2 = (f'{data[7]:,}'.replace(',', ' '))
        
    Linia1_string.set("Saldo rachunków :")
    Linia2_string.set("Rachunek bankowy :   " + dane1 + "  PLN")
    Linia3_string.set("Rachunek gieldowy :   " + dane2 + "  PLN")
    Linia4_string.set("|\n|\n|\n|\n|")
    
  
    Linia1 = Label(LogoFrame_2, textvariable=Linia1_string, bg="white", fg="#2B2B43", font=('Georgia 13 bold'))
    #Linia1.grid(row=0, column=1, sticky=W, padx=(15,0))
    Linia1.place(x=580,y=10)
    Linia2 = Label(LogoFrame_2, textvariable=Linia2_string, bg="white", fg="#2B2B43", font=('Georgia 13'))
    #Linia2.grid(row=1, column=1, sticky=W, padx=(15,0))
    Linia2.place(x=580,y=35)
    Linia3 = Label(LogoFrame_2, textvariable=Linia3_string, bg="white", fg="#2B2B43", font=('Georgia 13'))
    #Linia3.grid(row=2, column=1, sticky=W, padx=(15,0))
    Linia3.place(x=580,y=60)
    Linia4 = Label(LogoFrame_2, textvariable=Linia4_string, bg="white", fg="#c9c9e1")
    Linia4.place(x=560,y=10)
    ## - Koniec Lable Info --- ##

    ## - Button wyloguj --- ##
    def wyloguj_enter(e):
        wylogujBtn.configure(cursor='hand2')
        img_wyloguj.configure(file = f"img/wyloguj_hover.png")
        
    def wyloguj_button(e):
        main.destroy()

    def wyloguj_leave(e):
        img_wyloguj.configure(file = f"img/wyloguj.png")

    img_wyloguj = PhotoImage(file = f"img/wyloguj.png")
    wylogujBtn = Label(LogoFrame_3, image = img_wyloguj, bd=0)
    wylogujBtn.place(x=70,y=20)
    #wylogujBtn.grid(padx=(0,25))
    #wylogujBtn.configure(bg="white", width=200, anchor=E) #, state=NORMAL
    
    wylogujBtn.bind("<Enter>", wyloguj_enter)
    wylogujBtn.bind("<Leave>", wyloguj_leave)
    wylogujBtn.bind("<Button>", wyloguj_button)
    ## - Koniec Button wyloguj --- ##


    ### --------------------------- ### ------------------------------------------------------------------------- ###

    ### Main Frame --------------- ### -------------------------------------------------------------------------- ###
    ### --------------------------- ### ------------------------------------------------------------------------- ###
    ### --------------------------- ### ------------------------------------------------------------------------- ###

    MainFrame=Frame(main, width=1400,height=600, bg="lightblue")
    MainFrame.grid(row=2, column=0, sticky=NSEW)

    bg = PhotoImage(file="img/bg-main.png")
    
    my_canvas = Canvas(MainFrame, width=1400, height=600, highlightthickness=0)
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_image(0,0, image=bg, anchor=NW)
    my_canvas.create_text(50,30, text="Menu :", font=('Nunito 12'), fill="#2B2B43", anchor=NW)

    global frame_qty, konto_button, wplata_button, moje_konto_on, wplata_konto_on
    frame_qty = 0
    konto_button = 0
    wplata_button = 0
    moje_konto_on = False
    wplata_konto_on = False
    
    ## Frame section : ------------- MainFrameIn1 ------------------|
    ## -------------------------------------------------------------|

    def show_frame_moje_konto():
        img_moje_konto.configure(file= f"img/konto_button_hover.png")
        global frame_qty, konto_button ,MainFrameIn1, moje_konto_on
        frame_qty = 1
        konto_button = 1
        moje_konto_on = True

        MainFrameIn1 = Label(MainFrame, width=1000, height=550, bg="white")
        MainFrameIn1.place(x=380, y=20, width=1000, height=550)
        
        def hide_frame():
            MainFrameIn1.place_forget()
            global frame_qty, konto_button, moje_konto_on
            frame_qty = 0
            konto_button = 0
            img_moje_konto.configure(file = f"img/konto_button.png")
            moje_konto_on = False
            
        # Lstring1 = StringVar()
        # Lstring1.set("Konto numer :  " + str(data[4]))
        # L1 = Label(MainFrameIn1, textvariable=Lstring1, bg="white", fg="#2B2B43", font=('Georgia 12'))
        # L1.place(x=20,y=60)

        image = PhotoImage(file=f"img/img_textBox.png")
        label = Label(MainFrameIn1, bd=0, image=image)
        label.config(image=image)
        label.grid(row=0, column=0, padx=10, pady=10)

        
        #label.config(image=image)

        entry = Entry(MainFrameIn1, bd=0, font="Georgia 12", fg="#999999", background="white")
        entry.grid(row=0, column=0, padx=20, sticky=W)
        
        Button(MainFrameIn1, text=" Anuluj ", font="Georgia 12",  command=hide_frame).grid(row=1,column=0)

    # def show_frame_moje_konto():
    #     img_moje_konto.configure(file= f"img/konto_button_hover.png")
    #     global frame_qty, konto_button ,MainFrameIn1, moje_konto_on
    #     frame_qty = 1
    #     konto_button = 1
    #     moje_konto_on = True

    #     MainFrameIn1 = Canvas(MainFrame, width=1000, height=550, bg="white")
    #     MainFrameIn1.place(x=380, y=20)
        
    #     def hide_frame():
    #         MainFrameIn1.place_forget()
    #         global frame_qty, konto_button, moje_konto_on
    #         frame_qty = 0
    #         konto_button = 0
    #         img_moje_konto.configure(file = f"img/konto_button.png")
    #         moje_konto_on = False
            
    #     Lstring1 = StringVar()
    #     Lstring1.set("Konto numer :  " + str(data[4]))
    #     L1 = Label(MainFrameIn1, textvariable=Lstring1, bg="white", fg="#2B2B43", font=('Georgia 12'))
    #     L1.place(x=20,y=60)

    #     #entry11 = Entry(MainFrameIn1,text = "%s" %(data[5]) ,  bd = 1, bg = "white", foreground="blue", font=('Georgia 14'))
    #     #entry11.place(x = 400, y = 50, width = 272.0, height = 48)
        
    #     # ----------- TEST


    #     label = Label(MainFrameIn1)
    #     label.place

    #     image = PhotoImage(file=f"img/img_textBox.png")
    #     label.config(image=image)


    #     entry = Entry(MainFrameIn1, bd=0, font="Georgia 16")
    #     entry.grid(row=0, column=0)

    #     # ------------ END TEST

        
    #     #entry1_bg = MainFrameIn1.create_image(288.0, 38.0,image = entry_img)
        
    #     #entry_x1 = Entry(MainFrameIn1, background=entry_img) #bg = "#343f54" insertbackground="white", bd = 3,  , foreground="white", font=('Georgia 14'), highlightthickness = 0
    #     #entry_x1.place(x=200,y=10)

    #     Button(MainFrameIn1, text=" Anuluj ", font="Georgia 12",  command=hide_frame).place(x=920,y=500)

    ## Frame section : ------------- MainFrameIn2 ------------------|
    ## Wplata na konto - opcja 2
    ## -------------------------------------------------------------|
    def show_frame_wplata_konto():
        img_wplata_konto.configure(file= f"img/wplata_button_hover.png")
        global frame_qty, wplata_button ,MainFrameIn2 , wplata_konto_on
        frame_qty = 1
        wplata_button = 1
        wplata_konto_on = True

        MainFrameIn2 = Canvas(MainFrame, width=1000, height=550, bg="white")
        MainFrameIn2.place(x=380, y=20)
                
        def hide_frame2():
            MainFrameIn2.place_forget()
            global frame_qty, wplata_button, wplata_konto_on
            frame_qty = 0
            wplata_button = 0
            img_wplata_konto.configure(file = f"img/wplata_button.png")
            wplata_konto_on = False
            
        Lstring1 = StringVar()
        Lstring1.set("Wplata na konto")
        L1 = Label(MainFrameIn2, textvariable=Lstring1, bg="white", fg="#2B2B43", font=('Georgia 13 bold'))
        L1.place(x=20,y=20)

        Button(MainFrameIn2, text="Exit", fg="blue", font="Georgia 14 bold",  command=hide_frame2).place(x=550,y=400)


    ### --------------------------- ### ------------------------------------------------------------------------- ###

    def check():
        global MainFrameIn1, moje_konto_on, konto_button, MainFrameIn2, wplata_konto_on, wplata_button, frame_qty
        if moje_konto_on == True:
            MainFrameIn1.place_forget()
            frame_qty = 0
            konto_button = 0
            img_moje_konto.configure(file = f"img/konto_button.png")
            moje_konto_on = False

        if wplata_konto_on == True:
            MainFrameIn2.place_forget()
            frame_qty = 0
            wplata_button = 0
            img_wplata_konto.configure(file = f"img/wplata_button.png") 
            wplata_konto_on = False

        return

    ## - Menu Buttons ------------- ### ------------------------------------------------------------------------- ###
    ### --------------------------- ### ------------------------------------------------------------------------- ###
    ## - Menu buttons function --- ##
    ### --------------------------- ### ------------------------------------------------------------------------- ###

    def moje_konto_enter(e):
        if konto_button == 1:
            return
        moje_kontoBtn.configure(cursor='hand2')
        img_moje_konto.configure(file= f"img/konto_button_hover.png")
                
    def moje_konto_button(e):
        global konto_button
        check()
        if frame_qty == 0:
            konto_button = 1
            show_frame_moje_konto()
            #clear_MainFrameIn2()

    def moje_konto_leave(e):
        if konto_button == 1:
            return
        img_moje_konto.configure(file = f"img/konto_button.png")
    # |------------------------------------------------| 

    # |------------------------------------------------| 
    def wplata_konto_enter(e):
        if wplata_button == 1:
            return
        wplata_kontoBtn.configure(cursor='hand2')
        img_wplata_konto.configure(file = f"img/wplata_button_hover.png")

    def wplata_konto_button(e):
        global wplata_button
        check()
        if frame_qty == 0:
            wplata_button = 1
            show_frame_wplata_konto()

    def wplata_konto_leave(e):
        if wplata_button == 1:
            return
        img_wplata_konto.configure(file = f"img/wplata_button.png")
    # |------------------------------------------------| 

    
    ## - Menu buttons --- ##
        
    img_moje_konto = PhotoImage(file = f"img/konto_button.png")
    moje_kontoBtn = Label(my_canvas, image = img_moje_konto, bd=0)
    moje_kontoBtn.place(x=50,y=60)
    
    moje_kontoBtn.bind("<Enter>", moje_konto_enter)
    moje_kontoBtn.bind("<Leave>", moje_konto_leave)
    moje_kontoBtn.bind("<Button>", moje_konto_button)

    img_wplata_konto = PhotoImage(file = f"img/wplata_button.png")
    wplata_kontoBtn = Label(my_canvas, image = img_wplata_konto, bd=0)
    wplata_kontoBtn.place(x=50,y=140)
    
    wplata_kontoBtn.bind("<Enter>", wplata_konto_enter)
    wplata_kontoBtn.bind("<Leave>", wplata_konto_leave)
    wplata_kontoBtn.bind("<Button>", wplata_konto_button)
    # ## - Koniec Button wyloguj --- ##







    ### --------------------------- ### ------------------------------------------------------------------------- ###

    ### Bottom Frame -------------- ### ------------------------------------------------------------------------- ###

    BottomFrame=Frame(main,width=1400,height=50)
    BottomFrame.grid(row=3, column=0, sticky=NSEW)
    BottomFrame.configure(bg = "white")

    stringBottom1 = StringVar()
    stringBottom2 = StringVar()
    stringBottom1.set("Copyright 2022 Micro Bank")
    stringBottom2.set("Online Banking")

    stringBottom1 = Label(BottomFrame, textvariable=stringBottom1, bg="white", fg="#A5ADBD", font=('Georgia 12'))
    stringBottom1.place(x=15, y=10)

    stringBottom2 = Label(BottomFrame, textvariable=stringBottom2, bg="white", fg="#4E5F60", font=('Georgia 14'))
    stringBottom2.place(x=1250, y=10)
    
  

    ### --------------------------- ### ------------------------------------------------------------------------- ###

    main.resizable(False, False)
    main.mainloop()

### End of main TAB --------------------- ###


window.resizable(False, False)
window.mainloop()

