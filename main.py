import tkinter as tk
from tkinter import messagebox

def add_password():
    username = usernameInput.get()
    password = passwordInput.get()
    website = websiteInput.get()

    if not username or not password or not website:
        messagebox.showerror('Error', "Please fill in all fields.")
        return

    try:
        with open('passwords.yes', 'a') as passes:
            passes.write(f"Website: {website}, Username/Email: {username}, Password: {password}\n")
        print("Password added successfully.")
    except Exception as e:
        print(f"Failed to add password. Error: {e}")


app = tk.Tk()
app.geometry('800x450')
app.title('Password Manager')

def check_passes():
    try:
        with open('passwords.yes', 'r') as passes:
            data = passes.read()
            return data
    except FileNotFoundError:
        print('Creating a new file...')
        with open('passwords.txt', 'w') as newPassFile:
            data = ''
            return data

data = check_passes()

password_text = tk.Text(app, width=80, height=20)
password_text.insert(tk.END, data)
password_text.grid(columnspan=5)
password_text.config(state=tk.DISABLED) 

username_label = tk.Label(app, text='Username/Email:')
username_label.grid(row=1, column=0)
usernameInput = tk.Entry(app, width=35)
usernameInput.grid(row=1, column=1)

password_label = tk.Label(app, text='Password:')
password_label.grid(row=2, column=0)
passwordInput = tk.Entry(app, width=35)
passwordInput.grid(row=2, column=1)

website_label = tk.Label(app, text='Website:')
website_label.grid(row=3, column=0)
websiteInput = tk.Entry(app, width=35)
websiteInput.grid(row=3, column=1)

addButton = tk.Button(app, text='Add', width=35, command=add_password)
addButton.grid(row=4, column=1)

if __name__ == '__main__':
    app.mainloop()
