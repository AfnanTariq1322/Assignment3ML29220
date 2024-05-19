generator.py
----------------------
from tkinter import *
import random
import string
import secrets
import sqlite3
import database

connector = sqlite3.connect("passwords.db")
curs = connector.cursor()


# Function to create passwords
def generating(upper, lower, num, spec, word):
    txtOutput.delete(1.0, END)
    length = 1
    n = 0

    # Numbers
    digits = string.digits

    # Uppercase and lowercase letters
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase

    # Special characters
    symbols = "!#$%&()*+-./:;<=>?@\^_`|~"

    # User inputs
    upper = int(e1.get())
    lower = int(e2.get())
    num = int(e3.get())
    spec = int(e4.get())

    # Password name
    word = e5.get()

    n += upper + lower + num + spec
    if n < length:
        txtOutput.insert('1.0', "Password is too small")
        generating()
    else:
        new_password = ""
        for i in range(upper):
            new_password += random.choice(uppercase)
        for x in range(lower):
            new_password += random.choice(lowercase)
        for y in range(num):
            new_password += random.choice(digits)
        for z in range(spec):
            new_password += random.choice(symbols)

        pass_word = list(new_password)
        shuffling = random.shuffle(pass_word)
        new_pass = "".join(pass_word)
        password = secrets.token_urlsafe(7)

        curs.execute('SELECT Name FROM Passwords WHERE "Name"=?', (word,))
        data = str(curs.fetchone())
        if data == "None":
            curs.execute("INSERT OR IGNORE into Passwords (Name, Password) values (?, ?)",
                         (word, new_pass))
            connector.commit()
            txtOutput.insert('1.0', "Password name: " + word + "\n")
            txtOutput.insert('2.0', new_pass)
        else:
            txtOutput.delete(1.0, END)
            textbox2.delete(1.0, END)
            textbox2.insert('1.0', "Error. Password already exists.\nPlease choose another name or delete.\n")


# Function that quickly generates a 10 character password without the need for user inputs
def quick_generation():
    txtOutput.delete(1.0, END)
    # Numbers
    digits = string.digits

    # Uppercase and lowercase letters
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase

    # Special characters
    symbols = "!#$%&'()*+-./:;<=>?@\^_`|~"

    word = ''
    for i in range(2):
        word += random.choice(digits)
        word += random.choice(uppercase)
        word += random.choice(lowercase)
        word += random.choice(symbols)

    txtOutput.insert('1.0', word + "\n")


# Function that displays all saved passwords
def pulling():
    textbox2.delete(1.0, END)
    password = search_entry.get()
    curs.execute('SELECT Password FROM Passwords WHERE "Name"=?', (password,))
    connector.commit()
    records = str(curs.fetchall())
    formatted = ''.join(f for f in records if f not in '[]{})(')
    o = formatted.replace("'", "").replace('"', '')
    final = o.strip(',')

    textbox2.insert('1.0', final)


def deleting():
    textbox2.delete(1.0, END)
    pass_name = search_entry.get()
    curs.execute('DELETE FROM Passwords WHERE "Name"=?', (pass_name,))
    connector.commit()
    textbox2.insert('1.0', "Password has been successfully deleted")


# All graphical user interface code
top = Tk()
top.title("Password Generator")  # Program title
# Window size
top.geometry("500x500")

top.configure(bg='#9C95DC')

background_image = PhotoImage(file='background.png')
background_label = Label(top, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Entry labels
up = Label(top, text="Upper", font="Arial 11 bold italic", bg='#9C95DC').place(x=40, y=110)
low = Label(top, text="Lower", font="Arial 11 bold italic", bg='#9C95DC').place(x=40, y=135)
nums = Label(top, text="Numbers", font="Arial 11 bold italic", bg='#9C95DC').place(x=29, y=163)
specials = Label(top, text="Special", font="Arial 11 bold italic", bg='#9C95DC').place(x=36, y=192)
name = Label(top, text="Name", font="Arial 11 bold italic", bg='#9C95DC').place(x=40, y=218)

# Entry points
frame_one = Frame(top, bg='#000000', bd=4)
frame_one.place(relx=.35, rely=.217, relwidth=.30, relheight=.05, anchor='n')
e1 = Entry(frame_one, bg='#F2F3F4')
e1.place(relwidth=1, relheight=1)

frame_two = Frame(top, bg='#000000', bd=4)
frame_two.place(relx=.35, rely=.270, relwidth=.30, relheight=.05, anchor='n')
e2 = Entry(frame_two, bg='#F2F3F4')
e2.place(relwidth=1, relheight=1)

frame_three = Frame(top, bg='#000000', bd=4)
frame_three.place(relx=.35, rely=.323, relwidth=.30, relheight=.05, anchor='n')
e3 = Entry(frame_three, bg='#F2F3F4')
e3.place(relwidth=1, relheight=1)

frame_four = Frame(top, bg='#000000', bd=4)
frame_four.place(relx=.35, rely=.376, relwidth=.30, relheight=.05, anchor='n')
e4 = Entry(frame_four, bg='#F2F3F4')
e4.place(relwidth=1, relheight=1)

frame_five = Frame(top, bg='#000000', bd=4)
frame_five.place(relx=.35, rely=.429, relwidth=.30, relheight=.05, anchor='n')
e5 = Entry(frame_five, bg='#F2F3F4')
e5.place(relwidth=1, relheight=1)

# Button to generate passwords
generate_frame = Frame(top, bg='#000000', bd=2)
generate_frame.place(relx=.34, rely=.490, relwidth=.13, relheight=.05, anchor='n')
b1 = Button(generate_frame, text="Generate", font="Arial 8 bold", bg='#EDDEA4',
            command=lambda: generating(e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
b1.place(relwidth=1, relheight=1)

# Button to quickly generate a password
quick_frame = Frame(top, bg='#000000', bd=2)
quick_frame.place(relx=.75, rely=.303, relwidth=.15, relheight=.05, anchor='n')
b2 = Button(quick_frame, text="QUICK-GEN", font="Arial 8 bold", bg='#EDDEA4', command=lambda: (quick_generation()))
b2.place(relwidth=1, relheight=1)

# Display password
txt_frame = Frame(top, bg='#000000', bd=4)
txt_frame.place(relx=.75, rely=.36, relwidth=.45, relheight=.10, anchor='n')
txtOutput = Text(txt_frame, bg='#F2F3F4', font="Fixedsys 10 bold")
txtOutput.place(relwidth=1, relheight=1)

# Password Search Results
textbox2_frame = Frame(top, bg='#000000', bd=4)
textbox2_frame.place(relx=.49, rely=.67, relwidth=.78, relheight=.3, anchor='n')
textbox2 = Text(textbox2_frame, bg='#F2F3F4', font="Fixedsys 10 bold")
textbox2.place(relwidth=1, relheight=1)

# Button to search for a password
b3_frame = Frame(top, bg='#000000', bd=2)
b3_frame.place(relx=.462, rely=.61, relwidth=.12, relheight=.05, anchor='n')
b3 = Button(b3_frame, text="Search", font="Arial 8 bold", bg="#EDDEA4", command=lambda: pulling())
b3.place(relwidth=1, relheight=1)

# Button to delete passwords
b4_frame = Frame(top, bg='#000000', bd=2)
b4_frame.place(relx=.585, rely=.61, relwidth=.12, relheight=.05, anchor='n')
b4 = Button(b4_frame, text="Delete", font="Arial 8 bold", bg="#EDDEA4", command=lambda: deleting())
b4.place(relwidth=1, relheight=1)

# Entry point for password search
search_frame = Frame(top, bg='#000000', bd=4)
search_frame.place(relx=.25, rely=.61, relwidth=.30, relheight=.05, anchor='n')
search_entry = Entry(search_frame, bg='#F2F3F4')
search_entry.place(relwidth=1, relheight=1)

top.mainloop()

----------------------
database.py
----------------------

import sqlite3

# Creating database connection and cursor
connector = sqlite3.connect("passwords.db")
curs = connector.cursor()
# Creating the database if it does not already exist
creation = """
    CREATE TABLE IF NOT EXISTS Passwords (
    Name TEXT UNIQUE,
    Password TEXT
    )"""

curs.execute(creation)

# Committing the changes and closing
connector.commit()
connector.close()