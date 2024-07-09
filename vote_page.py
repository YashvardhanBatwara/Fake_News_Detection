import tkinter as tk
from tkinter import messagebox
import sqlite3  
from functions import Member
import datetime

def settlePaymentsFake(link): #when news is voted fake
    conn = sqlite3.connect('registration_data.db')
    cursor = conn.cursor()
    cursor.execute('''select address from news where link = ?''', (link,))
    publisher = cursor.fetchone()[0]
    cursor.execute('''select sum(amount) from votes where vote = 1 and link = ?''', (link,))
    totalGive = cursor.fetchone()[0]
    cursor.execute('''select sum(amount) from votes where vote = 0 and link = ?''', (link,))
    totalFavor = cursor.fetchone()[0]
    cursor.execute('''select address, amount from votes where vote = 0 and link = ?''', (link,))
    payto = cursor.fetchall()
    for i in range(len(payto)) :
        Member.pay_from_owner(payto[i][0], payto[i][1] + (payto[i][1]*totalGive)/(totalFavor))
    conn.commit()
    conn.close()
    
def settlePaymentsTrue(link): #when news is voted real
    conn = sqlite3.connect('registration_data.db')
    cursor = conn.cursor()
    cursor.execute('''select address from news where link = ?''', (link,))
    publisher = cursor.fetchone()[0]
    cursor.execute('''select sum(amount) from votes where vote = 0 and link = ?''', (link,))
    totalGive = cursor.fetchone()[0]
    cursor.execute('''select sum(amount) from votes where vote = 1 and link = ?''', (link,))
    totalFavor = cursor.fetchone()[0]
    cursor.execute('''select address, amount from votes where vote = 1 and link = ?''', (link,))
    payto = cursor.fetchall()
    cursor.execute('''select sensitivity from news where link = ?''', (link,))
    t = cursor.fetchone()[0]
    publisher_paid = 0
    if t == "Sensitive" :
        publisher_paid = 2
    else :
        publisher_paid = 1
    Member.pay_from_owner(publisher, publisher_paid + totalGive/2)
    for i in range(len(payto)) :
        Member.pay_from_owner(payto[i][0], payto[i][1] + (payto[i][1]*totalGive)/(totalFavor*2))
    conn.commit()
    conn.close()

def vote_news(link, vote, address, private_key):
    conn = sqlite3.connect('registration_data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS votes 
                                  (link TEXT, address TEXT, vote INTEGER, amount REAL)''')
    conn.commit()
    cursor.execute("SELECT address FROM votes WHERE link = ?", (link,))
    voted_users = cursor.fetchall()

    if any(user[0] == address for user in voted_users):
        messagebox.showerror("Error", "You have already voted for this news")
    else:
        cursor.execute("SELECT address FROM news WHERE link = ?", (link,))
        publisher = cursor.fetchone()

        if publisher and publisher[0] == address:
            messagebox.showerror("Error", "You cannot vote on your own news")
        else:
            status, amount = (Member.voteT(link, address, private_key)
                              if vote else Member.voteF(link, address, private_key))
            if status == -1:
                messagebox.showerror("Error", "Not enough balance to vote")
            elif status == 3:
                messagebox.showinfo("Voting Closed", "Voting already closed for the link")
            elif status == 0 or status == 1 or status == 2:
                cursor.execute('''CREATE TABLE IF NOT EXISTS votes 
                                  (link TEXT, address TEXT, vote INTEGER, amount REAL)''')
                
                conn.commit()
                cursor.execute("INSERT INTO votes VALUES (?, ?, ?, ?)", (link, address, int(vote), amount,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Voted Successfully")
                if status == 0:
                    settlePaymentsFake(link)
                elif status == 1:
                    settlePaymentsTrue(link)
            elif status == -5:
                messagebox.showerror("Error","Some error in blockchain")

def open_vote_page(address,link=""):
    def create_header(window):
        header_frame = tk.Frame(window)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Top-left label for the name
        conn = sqlite3.connect('registration_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM registrations WHERE address=?", (address,))
        result = cursor.fetchone()
        
        conn.close()
        name_label = tk.Label(header_frame, text=f"Name: {result[0]}")
        name_label.pack(side=tk.LEFT, padx=10, pady=5)

        rating = Member.getRating(address)  # Get the rating for the address
        rating_label = tk.Label(header_frame, text=f"Rating: {rating}")
        rating_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def vote_fake():
        link = link_entry.get()
        private_key = private_key_entry.get()
        if link:
            vote_news(link,0,address,private_key)
        else:
            messagebox.showerror("Error", "Please enter a news link")

    def vote_real():
        link = link_entry.get()
        private_key = private_key_entry.get()
        if link:
            vote_news(link,1,address,private_key)
        else:
            messagebox.showerror("Error", "Please enter a news link")

    def go_back():
        vote_window.destroy()
        # Perform actions to go back to the previous page or window
        import options
        options.open_news_page(address)

    def view_news(link):
        news = Member.viewNews(link)
        if news[0] == "0x0000000000000000000000000000000000000000":
            messagebox.showinfo("No News Found", "News has not been added to the platform yet")
        else:
            publisher_add = news[0]
            time = news[1]
            time_stamp = datetime.datetime.fromtimestamp(time)
            time = time_stamp.strftime("%d-%m-%Y at %H:%M:%S")
            status = news[2]
            typeS = news[4]

            conn = sqlite3.connect('registration_data.db')
            cursor = conn.cursor()
            cursor.execute("select name, organization from registrations where address = ?", (Member.findPublisher(link),))
            details = cursor.fetchone()
            conn.commit()
            conn.close()

            t = "Sensitive" if typeS == 0 else "Unsensitive"
            s = "Fake" if status == 0 else "Real" if status == 1 else "Unverified"
            info_str = f"Name: {details[0]}\nOrganization: {details[1]}\nPublished on: {time}\nStatus: {s}\nType: {t}"
            messagebox.showinfo("News Details", info_str)



    vote_window = tk.Tk()
    vote_window.title("Vote on News")

    create_header(vote_window)

    link_label = tk.Label(vote_window, text="Enter News Link:")
    link_label.pack()

    link_entry = tk.Entry(vote_window, width=40)
    link_entry.insert(0, link)
    link_entry.pack(pady=5)

    private_Key_label = tk.Label(vote_window, text="Enter Private Key:")
    private_Key_label.pack()

    private_key_entry = tk.Entry(vote_window, width=40)
    private_key_entry.pack(pady=5)

    view_news_button = tk.Button(vote_window, text="View News Info", command=lambda: view_news(link_entry.get()))
    view_news_button.pack(pady=5)

    real_button = tk.Button(vote_window, text="Vote Real", command=vote_real)
    real_button.pack(pady=5)

    fake_button = tk.Button(vote_window, text="Vote Fake", command=vote_fake)
    fake_button.pack(pady=10)

    back_button = tk.Button(vote_window, text="Back", command=go_back)
    back_button.pack(pady=5)

    # Set window size and position
    window_width = 500
    window_height = 500
    screen_width = vote_window.winfo_screenwidth()
    screen_height = vote_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    vote_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    vote_window.mainloop()

