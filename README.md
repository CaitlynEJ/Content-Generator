# Content-Generator
Project for CS361- Software Engineering 1
Written By Caitlyn Jameson

This program uses the following pacakges:
- tkinter
- requests
- bst (Beautiful Soup 4, must be installed)
- random
- csv

To run the program, run the command: 
python3 contentGenerator.py

at this time, running the command by passing in a csv file does not work. I am still trying to implement that functionality. 

Once the program is run, a GUI window pops up and the user many enter in a primary keyword and a secondary keyword. At this time, the primary keyword must begin with a capital letter. When the user clicks 'submit', the program will run and return a random paragraph containing both word and output it to the output window. At this time, the paragraph is not formatted to fit the window, but it is saved to a output.csv in the same directory. 

Other notes, the paragraph returned may include random footnotes from the original article. I am working on figuring out a way to scrub the paragraph to remove them. 
