import tkinter as tk
from tkinter import messagebox
import sqlite3
from functions import Member

def get_user_data(address):
    conn = sqlite3.connect('registration_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM registrations WHERE address=?", (address,))
    result = cursor.fetchone()
    
    conn.close()

    return result

def get_ratings():
    conn = sqlite3.connect('registration_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, address, organization FROM registrations")
    rows = cursor.fetchall()

    ratings = []
    for row in rows:
        name = row[0]
        address = row[1]
        organization = row[2]
        rating = Member.getRating(address) 
        ratings.append((name, organization, rating))

    conn.close()

    # Sort ratings in decreasing order based on the second element (rating)
    ratings.sort(key=lambda x: x[2], reverse=True)

    show_ratings(ratings)

def show_ratings(ratings):
    ratings_window = tk.Tk()
    ratings_window.title("Ratings")

    scrollbar = tk.Scrollbar(ratings_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(ratings_window, yscrollcommand=scrollbar.set,width=400)
    
    # Column headings
    listbox.insert(tk.END, f"{'Name': <20}{'Organization': <30}{'Rating': >10}")

    for name, organization, rating in ratings:
        formatted_data = f"{name: <20}{organization: <30}{rating: >10}"
        listbox.insert(tk.END, formatted_data)

    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=listbox.yview)

    # Set window size and position
    window_width = 500
    window_height = 500
    screen_width = ratings_window.winfo_screenwidth()
    screen_height = ratings_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    ratings_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    ratings_window.mainloop()

def open_news_page(user_address):
    def publish_news():
    # call publish_page and close this function
        news_page.destroy()
        import publish_page
        publish_page.open_publish_page(user_address)

    def vote_news():
        # Placeholder for voting on news
        news_page.destroy()
        import vote_page
        vote_page.open_vote_page(user_address)

    def view_latest_news():
        # Placeholder for viewing latest news
        news_page.destroy()
        import last20_page
        last20_page.open_last20_page(user_address)

    user_data = get_user_data(user_address)

    news_page = tk.Tk()
    news_page.title("News Actions")

    welcome_label = tk.Label(news_page, text=f"Welcome, {user_data[0]}", font=("Arial", 14, "bold"))
    welcome_label.pack(pady=10)
    user_rating = Member.getRating(user_address)
    rating_label = tk.Label(news_page, text=f"Your Rating: {user_rating}", font=("Arial", 12))
    rating_label.pack(pady=5)

    publish_button = tk.Button(news_page, text="Publish News", command=publish_news, width=20)
    publish_button.pack(pady=10)

    vote_button = tk.Button(news_page, text="Vote on News", command=vote_news, width=20)
    vote_button.pack(pady=10)

    view_button = tk.Button(news_page, text="View Latest News", command=view_latest_news, width=20)
    view_button.pack(pady=10)

    get_ratings_button = tk.Button(news_page, text="Show Top Ratings", command=get_ratings, width=20)
    get_ratings_button.pack(pady=10)

    # Set window size and position
    window_width = 600
    window_height = 500
    screen_width = news_page.winfo_screenwidth()
    screen_height = news_page.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    news_page.geometry(f'{window_width}x{window_height}+{x}+{y}')

    news_page.mainloop()
