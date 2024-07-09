import tkinter as tk
from tkinter import messagebox
import sqlite3
from types import new_class
from functions import Member
from datetime import datetime
import calendar
    

def open_publish_page(user_address):
    def create_header(window):
        header_frame = tk.Frame(window)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Top-left label for the name
        conn = sqlite3.connect('registration_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM registrations WHERE address=?", (user_address,))
        result = cursor.fetchone()
        
        conn.close()
        name_label = tk.Label(header_frame, text=f"Name: {result[0]}")
        name_label.pack(side=tk.LEFT, padx=10, pady=5)

        rating = Member.getRating(user_address)  # Get the rating for the address
        rating_label = tk.Label(header_frame, text=f"Rating: {rating}")
        rating_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def publish():
        news_link = link_entry.get()
        sensitivity = var.get()
        user_private_key = private_key_entry.get()
        if news_link and sensitivity and user_private_key:
            save_news(news_link, sensitivity, user_address, user_private_key)
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def go_back():
        publish_page.destroy()
        #open options page
        import options
        options.open_news_page(user_address)
    def save_news(link, sensitivity, user_address, private_key):
        date = datetime.utcnow()
        time = calendar.timegm(date.utctimetuple())
        time = int(time)
        if sensitivity == "Sensitive":
            status = Member.publishNewsS(user_address, link, time, private_key)
        else:
            status = Member.publishNewsU(user_address, link, time, private_key)

        if status == 0:
            messagebox.showerror("Error","Not enough balance to publish news")
        else:
            conn = sqlite3.connect('registration_data.db')
            cursor = conn.cursor()
            cursor.execute('''create table if not exists news (link TEXT, address TEXT, sensitivity TEXT)''')
            cursor.execute("insert into news values (?, ?, ?)", (link, user_address, sensitivity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Published News Successfully")
            go_back()
        
  

    publish_page = tk.Tk()
    publish_page.title("Publish News")

    create_header(publish_page)

    private_key_label = tk.Label(publish_page, text="Enter Private Key:")
    private_key_label.pack()

    private_key_entry = tk.Entry(publish_page, width=40, show="*")  # Masking the input
    private_key_entry.pack(pady=5)

    link_label = tk.Label(publish_page, text="Enter News Link:")
    link_label.pack()

    link_entry = tk.Entry(publish_page, width=40)
    link_entry.pack(pady=5)

    sensitivity_label = tk.Label(publish_page, text="Select Sensitivity:")
    sensitivity_label.pack()

    var = tk.StringVar()
    sensitive_button = tk.Radiobutton(publish_page, text="Sensitive", variable=var, value="Sensitive")
    sensitive_button.pack()

    unsensitive_button = tk.Radiobutton(publish_page, text="Unsensitive", variable=var, value="Unsensitive")
    unsensitive_button.pack()

    publish_button = tk.Button(publish_page, text="Publish", command=publish)
    publish_button.pack(pady=10)

    back_button = tk.Button(publish_page, text="Back", command=go_back)
    back_button.pack(pady=5)

    # Set window size and position
    window_width = 700
    window_height = 600
    screen_width = publish_page.winfo_screenwidth()
    screen_height = publish_page.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    publish_page.geometry(f'{window_width}x{window_height}+{x}+{y}')

    publish_page.mainloop()

