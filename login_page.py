import tkinter as tk
import sqlite3
from eth_account import Account
from tkinter import messagebox
from functions import Member

def open_login_page():
    def check_registration(address):
        conn = sqlite3.connect('registration_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT address FROM registrations WHERE address=?", (address,))
        result = cursor.fetchone()

        conn.close()

        return result is not None

    def r0_registration(address):
        if check_registration(address):
            conn = sqlite3.connect('registration_data.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM registrations WHERE address=?", (address,))

            conn.close()
            messagebox.showerror("Error", "Rating reached 0. Please re-register")
        else:
            messagebox.showerror("Error", "Account is not registered")

    def login():
        # Get private key and address from entry fields
        private_key = private_key_entry.get()
        address = address_entry.get()
        
        if private_key and address:
            val = Member.login(address, private_key)
            if val == 1:
                if check_registration(address):
                    messagebox.showinfo("Login Successful", "Login successful")
                    root.destroy()
                    import options
                    options.open_news_page(address)
                else:
                    messagebox.showerror("Error", "Account is not registered")
            elif val == 0:
                messagebox.showerror("Error", "Invalid private key or address")
            else:
                r0_registration(address)
                
        else :
            messagebox.showerror("Error", "Please fill in all fields")

            
    def register():
        # close this window and open registration window by importing it
        root.destroy()
        import registration_page
        registration_page.open_registration_page()


    # Create the main window
    root = tk.Tk()
    root.title("Fake News Detector Login")


    # Set window size and position
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Create a frame for the login form
    login_frame = tk.Frame(root, pady=10)
    login_frame.pack()

    # Create labels and entry fields for private key and address
    private_key_label = tk.Label(login_frame, text="Private Key:")
    private_key_label.pack()
    private_key_entry = tk.Entry(login_frame, show="*")  # Masking the input
    private_key_entry.pack()

    address_label = tk.Label(login_frame, text="Address:")
    address_label.pack()
    address_entry = tk.Entry(login_frame)
    address_entry.pack()

    # Create login and register buttons
    login_button = tk.Button(login_frame, text="Login", width=10, command=login)
    login_button.pack(pady=10)

    register_button = tk.Button(login_frame, text="Register", width=10, command=register)
    register_button.pack()

    # Run the application
    root.mainloop()