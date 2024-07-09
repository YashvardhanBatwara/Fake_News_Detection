import tkinter as tk
from tkinter import messagebox
import sqlite3
from functions import Member
import datetime
def check_voting_status(var):
    return Member.isActive(var)  # Replace this with your logic to determine if voting is open or closed

def open_last20_page(address):
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

    def go_back():
        last20_window.destroy()
        import options
        options.open_news_page(address)

    def view_news(link):
        news = Member.viewNews(link)
        if news[0] == "0x0000000000000000000000000000000000000000":
            messagebox.showinfo("No News Found", "News has not been added to the platform yet")
        else:
            publisher_add = news[0]
            time = news[1]
            #convert time to readable format
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

    def redirect_to_vote(link):
        voting_status = check_voting_status(link)
        if voting_status:
            last20_window.destroy()
            import vote_page
            vote_page.open_vote_page(address, link)
        else:
            messagebox.showinfo("Voting Closed", "Voting is closed for this news.")
    def news_check(link):
        news = Member.viewNews(link)
        if news[0] == "0x0000000000000000000000000000000000000000":
            return 0
        else:
            return 1
            
    last20_window = tk.Tk()
    last20_window.title("Last 20 News")

    create_header(last20_window)

    canvas = tk.Canvas(last20_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(last20_window, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    news_list = Member.getLast20()
    for i, news in enumerate(news_list):
        label = tk.Label(frame, text=f"News Link: {news}")
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        
        view_info_button_state = tk.NORMAL if news_check(news) else tk.DISABLED 
        view_info_button = tk.Button(frame, text="View Info",state = view_info_button_state, command=lambda n=news: view_news(n))
        view_info_button.grid(row=i, column=1, padx=5, pady=5)

        vote_button_state = tk.NORMAL if check_voting_status(news) else tk.DISABLED
        vote_button = tk.Button(frame, text="Vote", state=vote_button_state, command=lambda n=news: redirect_to_vote(n))
        vote_button.grid(row=i, column=2, padx=5, pady=5)

    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)

    back_button = tk.Button(last20_window, text="Back", command=go_back)
    back_button.pack(pady=10)

    last20_window.mainloop()

# Test example
# open_last20_page("0x123...")  # You can pass an array of news links here
