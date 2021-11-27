from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- Display ------------------------------- #


def delete_fields():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


def display_text(text):
    def clear():
        display.config(text="")
    display.config(text=text)
    display.after(1500, clear)


# ---------------------------- SEARCH ------------------------------- #


def search_command():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_final:
            all_websites = json.load(data_final)
            email_pass = all_websites[website.title()]
    except FileNotFoundError:
        messagebox.showinfo(title="No Data!!",
                                  message="Sorry You Have Not Save Any Passwords Till Now!")
        # delete_fields()
    except KeyError:
        messagebox.showinfo(title=f"No Data Found !!!",
                                  message=f"No Details For {website} Exist.")
    else:
        email_user = email_pass["Email"]
        password_user = email_pass["Password"]
        yes = messagebox.askokcancel(title=website,
                               message=f"Email: {email_user}\n"
                                       f"Password: {password_user}\n"
                                       f"Ok-To Copy Password\n"
                                       f"Cancel To Exit")
        if yes:
            display_text("Password Copied To Clipboard")
            pyperclip.copy(password_user)
        delete_fields()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


letters_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbols_list = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '-`', '}', '{', ':', '>', '<',
                '.', ',', ';']
numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def generate_password():
    user_let = random.randint(8, 10)
    user_spc = random.randint(2, 4)
    user_num = random.randint(2, 4)
    password_list1 = [letters_list[numb_index] for numb_index in range(0, user_let)]
    password_list2 = [symbols_list[numb_index] for numb_index in range(0, user_spc)]
    password_list3 = [numbers_list[numb_index] for numb_index in range(0, user_num)]
    final_password_list = (password_list1 + password_list2 + password_list3)
    random.shuffle(final_password_list)
    final_password = "".join(final_password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, final_password)
    pyperclip.copy(final_password)
    display_text("Copied! To Clipboard")
    # messagebox.askokcancel(title="Copied!!", message="We display password to your clipboard")
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_entry.get()
    user_name = email_entry.get()
    password = password_entry.get()
    user_details = {
        website.title().strip(): {
            "Email": user_name,
            "Password": password
        }
    }
    if len(website) == 0 or len(user_name) == 0 or len(password) == 0:
        messagebox.askretrycancel(title="Oops!!", message="You can't leave any field empty")
    else:
        is_ok = True
        display_text("Saved Your Credentials!!")
        if is_ok:
            try:
                with open(file="data.json", mode="r") as data_:
                    previous_data = json.load(data_)
            except FileNotFoundError:
                with open(file="data.json", mode="w") as data:
                    json.dump(user_details, data, indent=4)
            else:
                previous_data.update(user_details)
                with open(file="data.json", mode="w") as data:
                    json.dump(previous_data, data, indent=4)
            finally:
                delete_fields()
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=20, bg="#CDEDF6")

image_logo = PhotoImage(file="E:\shared folder to kali\python practice\day29\secure.png")

canvas = Canvas(width=250, height=250,  bg="#CDEDF6", highlightthickness=0)
canvas.create_image(125, 125, image=image_logo,)

# Labels
display = Label(text="", font=("Arial", 13, "bold"), pady=10, bg="#CDEDF6")
website_label = Label(text="Website:", font=("Arial", 13, "bold"), pady=10, bg="#CDEDF6")
email_label = Label(text="Email/User_name:", font=("Arial", 13, "bold"), pady=10, bg="#CDEDF6")
password_label = Label(text="Password:", font=("Arial", 13, "bold"), pady=10, bg="#CDEDF6")

# Entry

password_entry = Entry(width=40)
website_entry = Entry(width=40)
email_entry = Entry(width=63)

# Buttons

search = Button(width=14, text="Search", font=("Arial", 10, "bold"), command=search_command, bg="#F7EC59")
add = Button(width=36, text="Add", font=("Arial", 13, "bold"), command=save_password, bg="#A379C9")
gen_password = Button(width=16, text="Generate Password", font=("Arial", 10, "bold"), bg="#73937E", command=generate_password)

# Grids

canvas.grid(column=1, row=0)
password_label.grid(column=0, row=3)
email_label.grid(column=0, row=2)
website_label.grid(column=0, row=1)
website_entry.grid(column=1, row=1, padx=10)
search.grid(column=2, row=1,)
website_entry.focus()
email_entry.grid(column=1, row=2, columnspan=2)
password_entry.grid(column=1, row=3, pady=10)
gen_password.grid(column=2, row=3, columnspan=2, pady=10, padx=10)
add.grid(column=1, row=4, columnspan=2, pady=5)
display.grid(column=1, row=5, columnspan=2)
window.mainloop()
