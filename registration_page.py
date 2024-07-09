import tkinter as tk
from tkinter import messagebox
import sqlite3
from eth_account import Account  # Importing Ethereum account functions
from functions import Member

def open_registration_page():
    def validate_private_key(private_key, address):
        try:
            derived_address = Account.from_key(private_key).address
            return derived_address == address
        except Exception as e:
            return False

    def register():
        # Get registration information
        reg_address = address_entry.get()
        reg_private_key = private_key_entry.get()
        name = name_entry.get()
        organization = organization_entry.get()
        location = location_entry.get()

        if reg_address and reg_private_key and name and organization and location:
            if validate_private_key(reg_private_key, reg_address) and Member.register_payfees(reg_address, reg_private_key):
                # Save registration data to a SQLite database
                conn = sqlite3.connect('registration_data.db')
                cursor = conn.cursor()

                # Create a table if it doesn't exist
                cursor.execute('''CREATE TABLE IF NOT EXISTS registrations 
                                (address TEXT, name TEXT, organization TEXT, locX REAL, locY REAL)''')

                # Insert registration data into the table
                locx = 27.5
                locy = 80.5
                if(location == "Delhi"):
                    locx = 28.7041
                    locy = 77.1025
                elif(location == "Mumbai"):
                    locx = 19.0760
                    locy = 72.8777
                elif(location == "Kolkata"):
                    locx = 22.5726
                    locy = 88.3639
                elif(location == "Chennai"):
                    locx = 13.0827
                    locy = 80.2707
                elif(location == "Bangalore"):
                    locx = 12.9716
                    locy = 77.5946
                elif(location == "Hyderabad"):
                    locx = 17.3850
                    locy = 78.4867
                elif(location == "Ahmedabad"):
                    locx = 23.0225
                    locy = 72.5714
                elif(location == "Pilani"):
                    locx = 28.3639
                    locy = 77.5888
                cursor.execute("INSERT INTO registrations VALUES (?, ?, ?, ?, ?)",
                            (reg_address, name, organization,locx,locy,))

                conn.commit()
                conn.close()

                messagebox.showinfo("Registration Successful", "Registration successful")
                open_login()
            else:
                messagebox.showerror("Error", "Private key does not match the provided address or not enough balance to register.")
        else:
            messagebox.showerror("Error", "Please fill in all fields")


    def open_login():
        registration_window.destroy()
        import login_page
        login_page.open_login_page()

    def open_registration_window(parent):
        registration_window = tk.Tk()
        registration_window.title("Registration")

    # Create the registration window
    registration_window = tk.Tk()
    registration_window.title("Registration")

    # Set window size and position
    window_width = 600
    window_height = 500
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    registration_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Create a frame for the registration form
    registration_frame = tk.Frame(registration_window, pady=10)
    registration_frame.pack()

    # Create labels and entry fields for registration
    address_label = tk.Label(registration_frame, text="Address:")
    address_label.pack()
    address_entry = tk.Entry(registration_frame)
    address_entry.pack()

    private_key_label = tk.Label(registration_frame, text="Private Key:")
    private_key_label.pack()
    private_key_entry = tk.Entry(registration_frame, show="*")  # Masking the input
    private_key_entry.pack()

    name_label = tk.Label(registration_frame, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(registration_frame)
    name_entry.pack()

    organization_label = tk.Label(registration_frame, text="Organization:")
    organization_label.pack()
    organization_entry = tk.Entry(registration_frame)
    organization_entry.pack()

    location_label = tk.Label(registration_frame, text="Location:")
    location_label.pack()
    location_entry = tk.Entry(registration_frame)
    location_entry.pack()

    # Create register and back buttons
    register_button = tk.Button(registration_frame, text="Register", width=10, command=register)
    register_button.pack(pady=10)

    back_button = tk.Button(registration_frame, text="Back", width=10, command=open_login)
    back_button.pack()

    # Run the application
    registration_window.mainloop()
