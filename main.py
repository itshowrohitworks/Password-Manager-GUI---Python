import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # List comprehension:
    password_letters = [choice(letters) for _ in range(randint(0, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    e_pass.insert(0, password)
    pyperclip.copy(text=password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = e_web.get()
    email = e_email.get()
    password = e_pass.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password,
        }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website,message=f"These are the details entered: \nEmail: {email} \n Password: {password} \n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:

                    data = json.load(data_file)
            except FileNotFoundError:
                with open('data.json', 'w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open('data.json', 'w') as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                e_web.delete(0, END)
                e_pass.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = e_web.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data file found.")
    else:
        if website in data:
            email = data[website]['Email']
            password = data[website]['Password']
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)
# Labels:
website = Label(text='Website:', font=('Arial', 12))
website.grid(column=0, row=1)

email = Label(text='Email/Username:', font=('Arial', 12))
email.grid(column=0, row=2)

password = Label(text='Password:', font=('Arial', 12))
password.grid(column=0, row=3)

# Entries
e_web = Entry(width=21)
e_web.grid(row=1, column=1, sticky='EW')
e_web.focus()

e_email = Entry(width=35)
e_email.grid(row=2, column=1, columnspan=2, sticky='EW')
e_email.insert(0, "rohitshrivastava@gmail.com")

e_pass = Entry(width=33)
e_pass.grid(row=3, column=1)

# Buttons:
generate = Button(text="Generate Password",width=15, command=generate_password)
generate.grid(column=2, row=3)

add = Button(text="Add", width=36, command=save)
add.grid(column=1, row=4, columnspan=2, sticky='EW')

search = Button(text="Search",width=13,command=find_password)
search.grid(column=2,row=1)

window.mainloop()
