from typing import Text
from NYC_Commute_Assistant import *
from tkinter import * 
from tkinter.ttk import *

north_list = sofia_to_work()


# writing code needs to
# create the main window of 
# the application creating 
# main window object named root
root = Tk()
  
# giving title to the main window
root.title("First_Program")
  
# Label is what output will be 
# show on the window
label = Label(root, text="The next train to work will arrive to the station at: " + str(north_list[0])).pack()

label2 = Label(root, text="The next few trains will arrive at:").pack()

for x in range(1, len(north_list)):
    x = Label(label2, text=str(north_list[x])).pack() 
root.mainloop()