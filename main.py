from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()
    # data format to be added to the json file
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            # Saving updated data
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)  # indent 4 is the number of spaces for each indentation
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD --------------------------#


def find_password():
    website = website_entry.get().lower()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found!\nTry to Add data first.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=f"{website} info", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="info", message=f"No credentials were saved for this website: {website}")


# ---------------------------- ENCRYPTING & DECRYPTING --------------------------------#

def encrypt():
    print("encrypting...")
    # generate the key file named mykey.key
    # key = Fernet.generate_key()
    key = get_random_bytes(16)

    with open('mykey.key', 'wb') as mykey:
        mykey.write(key)
    print("key file generated successuly.")

    with open("data.json", "rb") as data_file:
        data = data_file.read()
    # data = b'secret data'

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    file_out = open("encrypted_data.json", "wb")
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()
    print("The file is encrypted successfuly.")


def decrypt():
    print("decrypting...")
    file_in = open("encrypted_data.json", "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]

    with open("mykey.key", "rb") as mykey_file:
        key = mykey_file.read()
    # let's assume that the key is somehow available again
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    # print(data)
    with open("decrypted_data.json", "wb") as decrypted_file:
        decrypted_file.write(data)
    print("The file is decrypted successfuly.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, sticky=W)
website_entry.focus()
email_entry = Entry(width=54)
email_entry.grid(row=2, column=1, columnspan=2, sticky=W)
email_entry.insert(0, "essalhi1234@gmail.com")
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, sticky=W)

# Buttons
generate_password_button = Button(text="Generate Password", width=15, command=generate_password)
generate_password_button.grid(row=3, column=2)
search_button = Button(text="Search", width=15, command=find_password)

add_button = Button(text="Add", width=46, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button.grid(row=1, column=2, sticky=W)

add_button = Button(text="Encrypt with AES", width=46, command=encrypt)
add_button.grid(row=5, column=1, columnspan=2)

add_button = Button(text="Decrypt", width=46, command=decrypt)
add_button.grid(row=6, column=1, columnspan=2)


window.mainloop()
