from tkinter import *

root = Tk()
root.title("Content Generator")

# define header
header = Label(root, text="Content Generator")

# define Input text box for primary keyword
primaryKeyword = Label(root, text="Please enter a primary keyword.")
inputBox1 = Entry(root, width=20, borderwidth=5)

# define input text box for secondary keyword
secondaryKeyword = Label(root, text="Please enter a secondary keyword.")
inputBox2 = Entry(root, width=20, borderwidth=5)

# define submit button
submitButton = Button(root, text="Click Me!")

# define output text box
outputBox = Entry(root, borderwidth=5)
resultHeader = Label(root, text="Results will be outputted below.")

# layout grid
header.grid(row=0, column=0)
primaryKeyword.grid(row=1, column=0)
inputBox1.grid(row=1, column=1)

secondaryKeyword.grid(row=2, column=0)
inputBox2.grid(row=2, column=1)

submitButton.grid(row=3, column=0)

resultHeader.grid(row=4, column=0)
outputBox.grid(row=5, column=0, columnspan=3,
               padx=10, pady=10, ipadx=100, ipady=50)


root.mainloop()