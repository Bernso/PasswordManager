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



password_text = tk.Text(app, width=80, height=20)
password_text.insert(tk.END, data)
password_text.grid(row=0, column=0)



if __name__ == '__main__':
    app.mainloop()
