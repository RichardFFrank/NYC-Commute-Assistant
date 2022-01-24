from NYC_Commute_Assistant import *
from tkinter import *
import tkinter
from PIL import ImageTk, Image
from time import sleep


north_list = generate_train_times()

def generate_times():
    while True:
        label = Label(window, text="The next train to work will arrive to the station at: " + str(north_list[0]))
        label.pack()

        for i in range(1, len(north_list)):
            label = Label(window, text=north_list[i])
            label.pack()
        sleep(60)

window = Tk()

window.title("When should I Leave?")

label1 = Label(window)
img = ImageTk.PhotoImage(Image.open("f-train.png"))
label1.configure(image=img)
label1.pack()

button = Button(window, text="Start Program", command=lambda:generate_times())
button.pack()

window.mainloop()











# # show on the window
# label = Label(root, text="The next train to work will arrive to the station at: " + str(north_list[0])).pack()

# label2 = Label(root, text="The next few trains will arrive at:").pack()

# for x in range(1, len(north_list)):
#     x = Label(label2, text=str(north_list[x])).pack() 
# root.mainloop()