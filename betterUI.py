try:
    import customtkinter as tk
    from tkinter import messagebox
    print("Successfully imported modules")
except ImportError as e:
    print(f"Error importing: {e}")

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
        messagebox.showinfo("Nice", "Password added successfully.")
        update_password_text()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add password. Error: {e}")

def update_password_text():
    content = check_passes()  # Get the data
    password_text.configure(state=tk.NORMAL)  # Set the state to NORMAL to allow editing
    password_text.delete(1.0, tk.END)  # Clear the current content
    password_text.insert(tk.END, content)  # Insert the updated content
    password_text.configure(state=tk.DISABLED)  # Set the state back to DISABLED

def check_passes():
    try:
        with open('passwords.yes', 'r') as passes:
            content = passes.read()
            return content
    except FileNotFoundError:
        print('Creating a new file...')
        with open('passwords.yes', 'w'):
            pass
        return ''

def remove_passwords():
    answer = messagebox.askyesno('Question', 'Are you sure you want to do this?')
    if not answer:
        return
    else:
        with open('passwords.yes', 'w') as passes:
            passes.write('')
        messagebox.showinfo("Done", "Passwords removed successfully.")
        update_password_text()

app = tk.CTk()
app.geometry('840x640')
app.title('Password Manager by Bernso')

# System settings
tk.set_appearance_mode("System")
tk.set_default_color_theme("blue")

data = check_passes()

tabs = tk.CTkTabview(master=app, width=800, height=600)
tabs.grid(row=0, column=0, padx=20, pady=20)

tabs.add("Add Pass")
tabs.add("View Pass")

addPassTab = tabs.tab("Add Pass")
viewPassTab = tabs.tab("View Pass")



# Add Password Tab
username_label = tk.CTkLabel(master=addPassTab, text='Username/Email:', font=('Arial', 30))
username_label.grid(row=1, column=0, padx=20, pady=10)
usernameInput = tk.CTkEntry(master=addPassTab, width=200)
usernameInput.grid(row=1, column=1, padx=20, pady=10, columnspan = 2)

password_label = tk.CTkLabel(master=addPassTab, text='Password:', font=('Arial', 30))
password_label.grid(row=2, column=0, padx=20, pady=10)
passwordInput = tk.CTkEntry(master=addPassTab, width=200)
passwordInput.grid(row=2, column=1, padx=20, pady=10, columnspan = 2)

website_label = tk.CTkLabel(master=addPassTab, text='Website:', font=('Arial', 30))
website_label.grid(row=3, column=0, padx=20, pady=10)
websiteInput = tk.CTkEntry(master=addPassTab, width=200)
websiteInput.grid(row=3, column=1, padx=20, pady=10, columnspan = 2)

addButton = tk.CTkButton(master=addPassTab, text='Add', width=100, height=25, command=add_password)
addButton.grid(row=4, column=1, pady=10)



# View Password Tab
wipeFileButton = tk.CTkButton(master=viewPassTab, text='Wipe Passwords', width=150, height=35, command=remove_passwords)
wipeFileButton.grid(row=1, column=0)

password_text = tk.CTkTextbox(master=viewPassTab, width=700, height=450)  # Adjust width and height accordingly
password_text.insert(tk.END, data)
password_text.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
password_text.configure(state=tk.DISABLED)



if __name__ == '__main__':
    app.mainloop()
    print("Bye")
