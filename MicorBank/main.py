from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk



def root():
    main.destroy()
    root = Tk()
    closeBtn = Button(root, text="Close", command=root.quit)
    closeBtn.pack(padx=30, pady=30)


main = Tk()
main.title('Micro Bank - Panel główny')

width = 1500 # Width 
height = 1000 # Height

screen_width = main.winfo_screenwidth()  # Width of the screen
screen_height = main.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
 
main.geometry('%dx%d+%d+%d' % (width, height, x, y))
main.configure(bg = "white")

### Logo Frame ---------------- ### ------------------------------------------------------------------------- ###
LogoFrame=Frame(main,width=1500,height=100)
LogoFrame.grid(row=0, column=0, sticky=NSEW)
LogoFrame.configure(bg = "white")

img_logo = PhotoImage(name="logo", file="img/img_logo.png")

label_logo = Label(LogoFrame, image=img_logo, bd=0, relief=SUNKEN)
#label_logo.grid_columnconfigure(0, weight=0)
label_logo.grid(row=0, column=0, padx=20, sticky=NSEW)
#label_logo.pack()



main.wm_attributes('-transparentcolor', '#ab23ff')

Label(LogoFrame, text= "This is a New line Text", font= ('Helvetica 18'), bg= '#ab23ff').place(x=0, y=0)





openBtn = Button(LogoFrame, text="Close", command=quit)
#openBtn.place(relx=850, rely=50, anchor=CENTER)
#openBtn.grid_columnconfigure(1, weight=1)
openBtn.grid(row=0, column=1, padx=1250) #sticky=tk.E
#openBtn.pack(padx=10, pady=10)

### --------------------------- ### ------------------------------------------------------------------------- ###

### Main Frame --------------- ### ------------------------------------------------------------------------- ###
MainFrame=Frame(main, width=1500,height=850)
MainFrame.grid(row=2, column=0, sticky=NSEW)



canvas_MF = Canvas(
    MainFrame,
    bg = "white",
    height = 850,
    width = 1500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")

canvas_MF.place(x = 0, y = 0)

background_img = PhotoImage(file = f"img/main-bg.png")
background = canvas_MF.create_image(
    750, 425,
    image=background_img)
### --------------------------- ### ------------------------------------------------------------------------- ###

### Bottom Frame -------------- ### ------------------------------------------------------------------------- ###

BottomFrame=Frame(main,width=1500,height=50)
BottomFrame.grid(row=3, column=0, sticky=NSEW)
BottomFrame.configure(bg = "white")
### --------------------------- ### ------------------------------------------------------------------------- ###

main.resizable(False, False)
main.mainloop()

