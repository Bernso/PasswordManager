try:
    import customtkinter as ctk
    import json
    import os
    from cryptography.fernet import Fernet, InvalidToken
    import tkinter as tk
    from tkinter import ttk, messagebox
    import pyperclip
    import webbrowser

except ImportError as e:
    print(f"Error importing: {e}") 
    input()
    quit()

# Constants
DATA_FILE = 'passwords.json'
KEY_FILE = 'DO_NOT_DELETE.key'

# Generate or load encryption key
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    return key

key = load_key()
cipher_suite = Fernet(key)

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            encrypted_data = json.load(file)
            data = []
            for entry in encrypted_data:
                try:
                    decrypted_password = cipher_suite.decrypt(entry['password'].encode()).decode()
                    data.append({'username': entry['username'], 
                                 'password': decrypted_password,
                                 'website': entry['website']})
                except (InvalidToken, TypeError, ValueError):
                    print("Error decrypting data, skipping entry")
                    continue
            return data
    return []

data = load_data()

def save_data():
    encrypted_data = [{'username': entry['username'], 
                       'password': cipher_suite.encrypt(entry['password'].encode()).decode(),
                       'website': entry['website']} for entry in data]
    with open(DATA_FILE, 'w') as file:
        json.dump(encrypted_data, file)

def add_password():
    username = entry_username.get()
    password = entry_password.get()
    website = entry_website.get()
    
    if username and password and website:
        data.append({'username': username, 'password': password, 'website': website})
        save_data()
        entry_username.delete(0, ctk.END)
        entry_password.delete(0, ctk.END)
        entry_website.delete(0, ctk.END)
        display_passwords()
    else:
        messagebox.showwarning("Error", "All fields must be filled out")

def search_passwords():
    search_term = entry_search.get().lower()
    results = [entry for entry in data if search_term in entry['website'].lower()]
    display_results(results)
    
    # Update search result label
    search_result_label.configure(text=f"{len(results)} results found")

def delete_password():
    deleteYesorNo = messagebox.askyesno("Confirmation", f"Are you sure you want to delete this password?")
    if deleteYesorNo:    
        selected_index = listbox.curselection()
        if selected_index:
            selected_text = listbox.get(selected_index[0])
            website = selected_text.split(' | ')[0].split(': ')[1]
            data[:] = [entry for entry in data if entry['website'] != website]
            save_data()
            display_passwords()

def view_password():
    selected_index = listbox.curselection()
    if selected_index:
        selected_text = listbox.get(selected_index[0])
        website = selected_text.split(' | ')[0].split(': ')[1]
        for entry in data:
            if entry['website'] == website:
                messagebox.showinfo("Password", f"Password: {entry['password']}\n^Copied to clipboard")
                pyperclip.copy(entry['password'])
                break

def display_passwords():
    listbox.delete(0, tk.END)
    for entry in data:
        listbox.insert(tk.END, f"Website: {entry['website']} | Username: {entry['username']}")

def display_results(results):
    listbox.delete(0, tk.END)
    for entry in results:
        listbox.insert(tk.END, f"Website: {entry['website']} | Username: {entry['username']}")

def openWebsite():
    selected_index = listbox.curselection()
    if selected_index:
        selected_text = listbox.get(selected_index[0])
        website = selected_text.split(' | ')[0].split(': ')[1]
        for entry in data:
            if entry['website'] == website:
                webbrowser.open(entry['website'])
                break

app = ctk.CTk()
app.geometry("600x700")
app.title("Advanced Password Manager")


# Tab control
tab_control = ttk.Notebook(app)
tab_control.pack(expand=1, fill='both')


# Add password tab
add_password_tab = ttk.Frame(tab_control)
tab_control.add(add_password_tab, text='Add Password')

# Search password tab
search_password_tab = ttk.Frame(tab_control)
tab_control.add(search_password_tab, text='Search Password')

# Display password tab
display_password_tab = ttk.Frame(tab_control)
tab_control.add(display_password_tab, text='View Passwords')



# Frame for Add Password tab
frame_add = ctk.CTkFrame(add_password_tab)
frame_add.pack(pady=20, padx=20, fill="both", expand=True)

label_username = ctk.CTkLabel(frame_add, text="Username:")
label_username.pack(pady=5)
entry_username = ctk.CTkEntry(frame_add, width=400)
entry_username.pack(pady=5)

label_password = ctk.CTkLabel(frame_add, text="Password:")
label_password.pack(pady=5)
entry_password = ctk.CTkEntry(frame_add, show='*', width=400)  # Masking password entry
entry_password.pack(pady=5)

label_website = ctk.CTkLabel(frame_add, text="Website:")
label_website.pack(pady=5)
entry_website = ctk.CTkEntry(frame_add, width=400)
entry_website.pack(pady=5)

button_add = ctk.CTkButton(frame_add, text="Add Password", command=add_password, width=300, height=35)
button_add.pack(pady=40)



# Frame for Search Password tab
frame_search = ctk.CTkFrame(search_password_tab)
frame_search.pack(pady=20, padx=20, fill="both", expand=True)

label_search = ctk.CTkLabel(frame_search, text="Search Website:")
label_search.pack(pady=5)
entry_search = ctk.CTkEntry(frame_search)
entry_search.pack(pady=5)
button_search = ctk.CTkButton(frame_search, text="Search", command=search_passwords)
button_search.pack(pady=5)

search_result_label = ctk.CTkLabel(frame_search, text="")
search_result_label.pack(pady=5)



# Frame for Display Passwords tab
frame_display = ctk.CTkFrame(display_password_tab)
frame_display.pack(pady=20, padx=20, fill="both", expand=True)

button_delete = ctk.CTkButton(frame_display, text="Delete Selected", command=delete_password)
button_delete.grid(row=0, column=0, padx=20, pady=20)

button_view = ctk.CTkButton(frame_display, text="View Password", command=view_password)
button_view.grid(row=0, column=1, padx=20, pady=20)

openWebsiteButton = ctk.CTkButton(frame_display, text="Open Website", command=openWebsite)
openWebsiteButton.grid(row=0, column=2, padx=20, pady=20)

label_output = ctk.CTkLabel(frame_display, text="Stored Passwords:")
label_output.grid(row=1, column=1)
listbox = tk.Listbox(frame_display, height=30, width=80)
listbox.grid(row=2, column=0, columnspan=3)




if __name__ == "__main__":
    display_passwords()
    app.mainloop()
