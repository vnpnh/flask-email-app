import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL')

class EmailApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Email Management App")
        self.geometry("500x400")

        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, expand=True)

        self.tab1 = tk.Frame(notebook, width=500, height=400)
        self.tab2 = tk.Frame(notebook, width=500, height=400)
        self.tab3 = tk.Frame(notebook, width=500, height=400)
        self.tab4 = tk.Frame(notebook, width=500, height=400)

        self.tab1.pack(fill="both", expand=True)
        self.tab2.pack(fill="both", expand=True)
        self.tab3.pack(fill="both", expand=True)
        self.tab4.pack(fill="both", expand=True)

        notebook.add(self.tab1, text="Add User")
        notebook.add(self.tab2, text="Add Event")
        notebook.add(self.tab3, text="Add Recipient")
        notebook.add(self.tab4, text="Add Email")

        self.create_add_user_form(self.tab1)
        self.create_add_event_form(self.tab2)
        self.create_add_recipient_form(self.tab3)
        self.create_add_email_form(self.tab4)

    def create_add_user_form(self, parent):
        """Create the form for adding a user"""
        tk.Label(parent, text="Add User", font=("Arial", 16)).pack(pady=10)

        tk.Label(parent, text="First Name").pack(pady=5)
        first_name_entry = tk.Entry(parent, width=40)
        first_name_entry.pack(pady=5)

        tk.Label(parent, text="Last Name").pack(pady=5)
        last_name_entry = tk.Entry(parent, width=40)
        last_name_entry.pack(pady=5)

        tk.Label(parent, text="Email").pack(pady=5)
        email_entry = tk.Entry(parent, width=40)
        email_entry.pack(pady=5)

        def submit_user():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            if first_name  and last_name and email:
                data = {"first_name": first_name, "last_name": last_name, "email_address": email}
                response = requests.post(f"{API_BASE_URL}/user", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "User added successfully!")
                    first_name_entry.delete(0, tk.END)
                    last_name_entry.delete(0, tk.END)
                    email_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", response.json().get("message"))
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        tk.Button(parent, text="Submit", command=submit_user).pack(pady=20)

    def create_add_event_form(self, parent):
        """Create the form for adding an event"""
        tk.Label(parent, text="Add Event", font=("Arial", 16)).pack(pady=10)

        tk.Label(parent, text="Event Title").pack(pady=5)
        title_entry = tk.Entry(parent, width=40)
        title_entry.pack(pady=5)

        tk.Label(parent, text="Event Description").pack(pady=5)
        description_entry = tk.Entry(parent, width=40)
        description_entry.pack(pady=5)

        tk.Label(parent, text="Event Date (YYYY-MM-DD)").pack(pady=5)
        date_entry = tk.Entry(parent, width=40)
        date_entry.pack(pady=5)

        def submit_event():
            title = title_entry.get()
            description = description_entry.get()
            date = date_entry.get()
            if title and date:
                data = {"event_name": title,"event_description": description ,"event_date": date}
                response = requests.post(f"{API_BASE_URL}/event", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Event added successfully!")
                    title_entry.delete(0, tk.END)
                    description_entry.delete(0, tk.END)
                    date_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", response.json().get("message"))
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        tk.Button(parent, text="Submit", command=submit_event).pack(pady=20)

    def create_add_recipient_form(self, parent):
        """Create the form for adding a recipient"""
        tk.Label(parent, text="Add Recipient", font=("Arial", 16)).pack(pady=10)

        tk.Label(parent, text="User IDs (comma-separated)").pack(pady=5)
        user_id_entry = tk.Entry(parent, width=40)
        user_id_entry.pack(pady=5)

        tk.Label(parent, text="Event ID").pack(pady=5)
        event_id_entry = tk.Entry(parent, width=40)
        event_id_entry.pack(pady=5)

        def submit_recipient():
            user_ids = user_id_entry.get()
            user_id_list = [int(user_id.strip()) for user_id in user_ids.split(",")]
            event_id = event_id_entry.get()
            if user_id_list and event_id:
                data = {"user_id": user_id_list, "event_id": int(event_id)}
                response = requests.post(f"{API_BASE_URL}/recipient", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Recipient added successfully!")
                    user_id_entry.delete(0, tk.END)
                    event_id_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", response.json().get("message"))
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        tk.Button(parent, text="Submit", command=submit_recipient).pack(pady=20)

    def create_add_email_form(self, parent):
        """Create the form for adding an email"""
        tk.Label(parent, text="Add Email", font=("Arial", 16)).pack(pady=10)

        tk.Label(parent, text="Event ID").pack(pady=5)
        event_entry = tk.Entry(parent, width=40)
        event_entry.pack(pady=5)

        tk.Label(parent, text="Subject").pack(pady=5)
        subject_entry = tk.Entry(parent, width=40)
        subject_entry.pack(pady=5)

        tk.Label(parent, text="Content").pack(pady=5)
        content_entry = tk.Entry(parent, width=40)
        content_entry.pack(pady=5)

        tk.Label(parent, text="Scheduled At (YYYY-MM-DD HH:MM)").pack(pady=5)
        scheduled_at_entry = tk.Entry(parent, width=40)
        scheduled_at_entry.pack(pady=5)

        def submit_email():
            event = event_entry.get()
            subject = subject_entry.get()
            content = content_entry.get()
            scheduled_at = scheduled_at_entry.get()
            if event_entry and subject and content and scheduled_at:
                data = {"event_id": event, "email_subject": subject, "email_content": content, "scheduled_at": scheduled_at}
                response = requests.post(f"{API_BASE_URL}/save_emails", json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Email added successfully!")
                    event_entry.delete(0, tk.END)
                    subject_entry.delete(0, tk.END)
                    content_entry.delete(0, tk.END)
                    scheduled_at_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", response.json().get("message"))
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        tk.Button(parent, text="Submit", command=submit_email).pack(pady=20)


if __name__ == '__main__':
    app = EmailApp()
    app.mainloop()
