import tkinter as tk

app = tk.Tk()
app.geometry('800x450')
app.title('Password Manager')

try:
    with open('passwords.txt', 'r') as passes:
        data = passes.read()
        passes.close()
except FileNotFoundError as e:
    print(f'Could not find file: {e}\nCreating a new file...')
    with open('passwords.txt', 'w') as newPassFile:
        data = ""
        newPassFile.close()

def save_password():
    with open('passwords.txt', 'w') as newPassFile:
        newPassFile.write(password_text.get(1.0, tk.END))
        newPassFile.close()

password_text = tk.Text(app, width=80, height=20)
password_text.insert(tk.END, data)
password_text.grid(columnspan=5)

usernameLabel = tk.Label(app, text='Username')
usernameLabel.grid(row=1, column=0)

usernameInput = tk.Entry(app, width=35)
usernameInput.grid(row=1, column=1)

passwordLabel = tk.Label(app, text='Password')
passwordLabel.grid(row=2, column=0)

passwordInput = tk.Entry(app, width=35)
passwordInput.grid(row=2, column=1)

websiteLabel = tk.Label(app, text='Website')
websiteLabel.grid(row=3, column=0)

websiteInput = tk.Entry(app, width=35)
websiteInput.grid(row=3, column=1)

addButton = tk.Button(app, text='Add', width=15, command=save_password)
addButton.grid(row=4, column=1)

if __name__ == '__main__':
    app.mainloop()
