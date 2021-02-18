from tkinter import *
import requests
from bs4 import BeautifulSoup
import random
import csv


# define generateParagrah function
def generateParagraph():
    primaryKey = inputBox1.get()
    secondKey = inputBox2.get()
    status = -1
    global output

    # find a wikipedia page about a topic
    response = requests.get(
        url="http://en.wikipedia.org/wiki/" + primaryKey,
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    # collect all paragraphs
    allParagraphs = soup.find_all('p')
    #generate random paragraph order
    random.shuffle(allParagraphs)
    for paragraph in allParagraphs:

        textPar = paragraph.text
        # determine if primary key and second key are in the paragraph
        if ((textPar.find(primaryKey) != -1) and (textPar.find(secondKey) != -1)):
            output = textPar
            status = 1
            break
        else:
            continue

    if status != 1:
        output = "We could not find context that contains those two words. Please try again."
        outputBox.insert(0, output)

    if status != -1:
        fields = ['input_words', 'output_content']
        rows = [(primaryKey + "; " + secondKey), output]
        outputBox.insert(0, output)
        filename = "output.csv"
        with open(filename, 'w') as csvfile:
            csvWrite = csv.writer(csvfile)

            csvWrite.writerow(fields)

            csvWrite.writerow(rows)


def main():

    # define GUI window
    root = Tk()
    root.title("Content Generator")

    global inputBox1
    global inputBox2
    global outputBox


    # define header
    header = Label(root, text="Content Generator")

    inputFrame = LabelFrame(root, padx=10, pady=10)
    outputFrame = LabelFrame(root, padx=10, pady=10, )

    # define Input text box for primary keyword
    primaryKeyword = Label(inputFrame, text="Please enter a primary keyword.")
    inputBox1 = Entry(inputFrame, width=20, borderwidth=5)

    # define input text box for secondary keyword
    secondaryKeyword = Label(inputFrame, text="Please enter a secondary keyword.")
    inputBox2 = Entry(inputFrame, width=20, borderwidth=5)

    # define submit button
    submitButton = Button(inputFrame, text="Submit Keywords!",
                          command=generateParagraph)


    # define output text box
    outputBox = Entry(outputFrame, borderwidth=5, )
    s = Scrollbar(outputFrame)

    resultHeader = Label(outputFrame, text="Generated results:")

    # layout grid
    inputFrame.grid(row=0, column=0, padx=10, pady=10)
    outputFrame.grid(row=1, column=0, padx=10, pady=10)

    header.grid(row=0, column=0)
    primaryKeyword.grid(row=1, column=0)
    inputBox1.grid(row=1, column=1)

    secondaryKeyword.grid(row=2, column=0)
    inputBox2.grid(row=2, column=1)

    submitButton.grid(row=3, column=1)

    resultHeader.grid(row=4, column=0)
    outputBox.grid(row=5, column=0, columnspan=3,
                   padx=10, pady=10, ipadx=100, ipady=50)


    root.mainloop()


if __name__ == '__main__':
    main()