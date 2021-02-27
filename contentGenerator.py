from tkinter import *
import requests
from bs4 import BeautifulSoup
import random
import csv
import sys
import socket


# define generateParagraph function
def generateParagraphGUI():
    """
    A function that gathers input from the GUI window, finds a matching wikipedia artcle, and then returns
    a paragraph containing both inputted words. The returned paragraph is also written to a 'output.csv' file.
    """
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
        output = "We could not find a paragraph that contains those two words. Please try again."
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


def generateParagraph(primaryKey, secondKey):
    """
    This function is the same as the GUI version, but without sending the found paragraph to the output box.
    This function takes as parameters a primary key and a secondary key passed via a .csv file, and writes the found
    content to a 'output.csv' file.
    """
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

    # no matching content found
    if status != 1:
        output = "We could not find context that contains those two words. Please try again."
        print(output)

    # content found and written to an output file.
    if status != -1:
        fields = ['input_words', 'output_content']
        rows = [(primaryKey + "; " + secondKey), output]
        filename = "output.csv"
        with open(filename, 'w') as csvfile:
            csvWrite = csv.writer(csvfile)

            csvWrite.writerow(fields)

            csvWrite.writerow(rows)

def request_content():
    """This function will be used with a population generator to request information about a State's  popluation for a
    given year"""

    request_list = []
    request_list.append(inputBox1)
    request_list.append(opt)
    host = "localhost"
    port = 32678
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
    mySocket.sendall(str(request_list).encode())
    response = mySocket.recv(1024)
    print(str(response, "utf-8"))
    mySocket.close
    return

def listen_for_request():
    """
    This functions listens for a reqeust from another program to return data to.
    """
    host = "localhost"
    port = 32678

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind((host, port))

    mySocket.listen()

    conn, addr = mySocket.accept()
    print("Connected by " + str(addr) + "\n")

    recv_data = conn.recv(1024)
    recv_data = recv_data.decode()
    recv_data = eval(recv_data)

    print(recv_data)

    conn.sendall(str(generateParagraph(recv_data[0],recv_data[1])).encode())

    conn.close()
    mySocket.close()

    return

def requestData():
    """A helper function to call both the generateParagraph function and the request_content function."""
    request_content()
    generateParagraphGUI()


def main():
    # define GUI window
    root = Tk()
    root.title("Content Generator")

    #define GUI text boxes
    global inputBox1
    global inputBox2
    global year
    global outputBox
    global opt

    yearList = []
    for year in range(2009, 2020):
        yearList.append(year)


    # define header
    header = Label(root, text="Content Generator")

    inputFrame = LabelFrame(root, padx=10, pady=10)
    outputFrame = LabelFrame(root, padx=10, pady=10, )

    # define Input text box for primary keyword
    primaryKeyword = Label(inputFrame, text="Please enter a state to be used as a primary Keyword.")
    inputBox1 = Entry(inputFrame, width=20, borderwidth=5)

    # define input text box for secondary keyword
    secondaryKeyword = Label(inputFrame, text="Please enter a secondary keyword.")
    inputBox2 = Entry(inputFrame, width=20, borderwidth=5)

    #define year dropdown
    yearLabel = Label(inputFrame, text="Please select a year.")
    year = StringVar(inputFrame)
    year.set(yearList[0])
    opt = OptionMenu(inputFrame, year, *yearList)

    # define submit button
    submitButton = Button(inputFrame, text="Request Content",
                          command=requestData)

    #define listen for reqeust
    listenButton = Button(inputFrame, text="Listen for Request", command=listen_for_request)


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

    yearLabel.grid(row=3, column=0)
    opt.grid(row=3, column=1)

    submitButton.grid(row=4, column=1)
    listenButton.grid(row=5, column=1)

    resultHeader.grid(row=6, column=0)
    outputBox.grid(row=7, column=0, columnspan=3,
                   padx=10, pady=10, ipadx=100, ipady=50)

    # call GUI window
    root.mainloop()


if __name__ == '__main__':
    # if program is called with a file for input
    if len(sys.argv) > 1:
        file = sys.argv[1]
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1

                else:

                    words = row[0].split(";")
                    primaryKey = words[0]
                    secondKey = words[1]

                    generateParagraph(primaryKey, secondKey)

    # GUI for manual user input
    else:
        main()
