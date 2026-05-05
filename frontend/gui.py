import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import requests
import os

from frontend.sync import start_auto_sync
from frontend.data_service import (
    login, register,
    get_users, delete_user,
    get_landlords, delete_landlord,
    get_customers, delete_customer
)

# ================= THEME =================
BG          =   "#0f1115"
CARD        =   "#161a22"
ACCENT      =   "#3b82f6"
DANGER      =   "#ef4444"
TEXT        =   "#e5e7eb"
SUBTEXT     =   "#9ca3af"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ================= APP =================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Offline Sync App")
        self.geometry("1000x600")
        self.configure(fg_color=BG)

        start_auto_sync()

        self.login_frame = LoginFrame(self)
        self.dashboard_frame = DashboardFrame(self)

    def show_dashboard(self, username):
        self.login_frame.pack_forget()
        self.dashboard_frame.set_user(username)
        self.dashboard_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)


# ================= LOGIN =================
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)
        self.pack(fill="both", expand=True)

        # ================= CARD =================
        container = ctk.CTkFrame(
            self,
            width=420,
            height=500,
            corner_radius=20,
            fg_color="#161a22"
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        # ================= LOGO =================
        try:
            import os
            from PIL import Image

            img_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "assets",
                "logo.jpeg"
            )

            image   = Image.open(img_path)
            logo    = ctk.CTkImage(image, size=(120, 60))

            ctk.CTkLabel(
                container,
                image=logo,
                text=""
            ).pack(pady=(25, 10))

        except Exception as e:
            print("Logo not found:", e)

        # ================= TITLE =================
        ctk.CTkLabel(
            container,
            text="Welcome Back 👋",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        ).pack(pady=(5, 5))

        ctk.CTkLabel(
            container,
            text="Login to continue",
            font=("Segoe UI", 14),
            text_color="#9ca3af"
        ).pack(pady=(0, 20))

        # ================= USERNAME =================
        self.user = ctk.CTkEntry(
            container,
            placeholder_text="Username",
            width=300,
            height=45,
            corner_radius=12,
            fg_color="#0f1115",
            border_width=1,
            border_color="#2b2f3a"
        )
        self.user.pack(pady=10)

        # ================= PASSWORD =================
        self.pwd = ctk.CTkEntry(
            container,
            placeholder_text="Password",
            show="*",
            width=300,
            height=45,
            corner_radius=12,
            fg_color="#0f1115",
            border_width=1,
            border_color="#2b2f3a"
        )
        self.pwd.pack(pady=10)

        # ================= ERROR LABEL =================
        self.result = ctk.StringVar()
        ctk.CTkLabel(
            container,
            textvariable=self.result,
            text_color="#ef4444"
        ).pack(pady=5)

        # ================= LOGIN BUTTON =================
        ctk.CTkButton(
            container,
            text="LOGIN",
            width=300,
            height=45,
            corner_radius=12,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 14, "bold"),
            command=self.do_login
        ).pack(pady=(15, 10))

        # ================= REGISTER BUTTON =================
        ctk.CTkButton(
            container,
            text="Create New Account",
            width=300,
            height=40,
            corner_radius=12,
            fg_color="transparent",
            border_width=1,
            border_color="#3b82f6",
            hover_color="#1f2937",
            command=self.do_register
        ).pack(pady=5)

    # ================= LOGIN LOGIC =================
    def do_login(self):
        from frontend.data_service import login

        res = login(self.user.get(), self.pwd.get())

        if res.get("status") == "success":
            self.master.show_dashboard(self.user.get())
        else:
            self.result.set(res.get("message"))

    # ================= REGISTER LOGIC =================
    def do_register(self):
        from frontend.data_service import register

        res = register(self.user.get(), self.pwd.get())
        self.result.set(res.get("message"))

# ================= DASHBOARD =================
class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        # Sidebar
        self.sidebar    = ctk.CTkFrame(self, width=200, fg_color=CARD)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="MENU",
                     text_color=SUBTEXT).pack(pady=(20, 10))

        self.nav_btn(" Users", self.show_users)
        self.nav_btn(" Customers", self.show_customers)
        self.nav_btn(" Landlords", self.show_landlords)
        self.nav_btn(" Profile", self.show_profile)

        ctk.CTkButton(self.sidebar, text=" Logout",
                      fg_color=DANGER,
                      command=self.logout).pack(pady=30, padx=10, fill="x")

        # Main
        self.main       =   ctk.CTkFrame(self, fg_color=BG)
        self.main.pack(side="left", fill="both", expand=True)

        # Header
        self.header      =  ctk.CTkFrame(self.main, height=60, fg_color="#12161d")
        self.header.pack(fill="x")

        self.title_label  =  ctk.CTkLabel(self.header,
                                        text="Dashboard",
                                        font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side="left", padx=20)

        self.content = ctk.CTkFrame(self.main, fg_color=BG)
        self.content.pack(fill="both", expand=True)

        self.username = ""

    def nav_btn(self, text, cmd):
        ctk.CTkButton(self.sidebar, text=text,
                      fg_color="transparent",
                      hover_color="#1f2630",
                      anchor="w",
                      command=cmd).pack(fill="x", padx=10, pady=5)

    def set_title(self, text):
        self.title_label.configure(text=text)

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def set_user(self, username):
        self.username = username

    # ================= USERS =================
    def show_users(self):
        self.set_title("Users")
        self.clear()

        for u in get_users():
            uid, uname = u

            card = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=10)
            card.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(card, text=uname,
                         font=("Segoe UI", 14)).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(card, text="Delete",
                          fg_color=DANGER,
                          command=lambda i=uid: self.remove_user(i)
                          ).pack(side="right", padx=10)

    def remove_user(self, uid):
        if messagebox.askyesno("Confirm", "Delete this user?"):
            delete_user(uid)
            self.show_users()



    
    # ================= CUSTOMERS =================
    def show_customers(self):
        self.set_title("Customers")
        self.clear()

        top = ctk.CTkFrame(self.content, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            top,
            text="➕ Add Customer",
            fg_color=ACCENT,
            command=self.show_add_customer_form
        ).pack(side="left")

        scroll = ctk.CTkScrollableFrame(self.content, fg_color=BG)
        scroll.pack(fill="both", expand=True)

        customers = get_customers()

        if not customers:
            ctk.CTkLabel(scroll, text="No customers found").pack(pady=20)
            return

        for c in customers:
            card = ctk.CTkFrame(scroll, fg_color=CARD)
            card.pack(fill="x", padx=20, pady=8)

            name = f"{c.get('first_name','')} {c.get('last_name','')}"

            ctk.CTkLabel(card, text=name).pack(side="left", padx=15)

            ctk.CTkButton(
                card,
                text="Delete",
                fg_color=DANGER,
                command=lambda i=c["id"]: self.remove_customer(i)
            ).pack(side="right")

    def remove_customer(self, cid):
        delete_customer(cid)
        self.show_customers()

    # ===== CUSTOMER ADD FORM =====
    def show_add_customer_form(self):
        self.set_title("Add Customer")
        self.clear()

        box = ctk.CTkFrame(self.content, fg_color=CARD)
        box.place(relx=0.5, rely=0.5, anchor="center")

        def field(label):
            ctk.CTkLabel(box, text=label).pack(anchor="w", padx=10)
            e = ctk.CTkEntry(box, width=300)
            e.pack(padx=10, pady=5)
            return e

        self.c_fname = field("First Name")
        self.c_lname = field("Last Name")
        self.c_email = field("Email")
        self.c_phone = field("Phone")

        ctk.CTkButton(
            box,
            text="Save",
            fg_color=ACCENT,
            command=self.add_customer
        ).pack(pady=10)

        ctk.CTkButton(
            box,
            text="Back",
            command=self.show_customers
        ).pack()

    def add_customer(self):
        data = {
            "first_name": self.c_fname.get(),
            "last_name": self.c_lname.get(),
            "email": self.c_email.get(),
            "phone": self.c_phone.get()
        }

        requests.post("http://127.0.0.1:5000/customers", json=data)
        self.show_customers()


    # ================= LANDLORDS =================
    def show_landlords(self):
        self.set_title("Landlords")
        self.clear()

        top = ctk.CTkFrame(self.content, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(top, text="➕ Add Landlord",
                      fg_color=ACCENT,
                      command=self.show_add_landlord_form).pack(side="left")

        self.list_frame = ctk.CTkFrame(self.content, fg_color=BG)
        self.list_frame.pack(fill="both", expand=True)

        self.load_landlords()

    def load_landlords(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        try:
            landlords = requests.get("http://127.0.0.1:5000/landlords").json()
        except:
            landlords = []

        if not landlords:
            ctk.CTkLabel(self.list_frame, text="No landlords found").pack(pady=20)
            return

        for l in landlords:
            card = ctk.CTkFrame(self.list_frame, fg_color=CARD, corner_radius=10)
            card.pack(fill="x", padx=20, pady=8)

            name = f"{l['first_name']} {l['last_name']}"

            ctk.CTkLabel(card, text=name,
                         font=("Segoe UI", 14)).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(card, text="Delete",
                          fg_color=DANGER,
                          command=lambda i=l["id"]: self.remove_landlord(i)
                          ).pack(side="right", padx=10)

    def remove_landlord(self, lid):
        delete_landlord(lid)
        self.load_landlords()

    # ================= ADD FORM =================
    def show_add_landlord_form(self):
        self.set_title("Add Landlord")
        self.clear()

        container = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=15)
        container.place(relx=0.5, rely=0.5, anchor="center")

        def field(label):
            ctk.CTkLabel(container, text=label).pack(anchor="w", padx=20)
            e = ctk.CTkEntry(container, width=300)
            e.pack(pady=5, padx=20)
            return e

        self.fname = field("First Name")
        self.lname = field("Last Name")
        self.company = field("Company")
        self.luser = field("Username")
        self.lpass = field("Password")
        self.phone = field("Phone")
        self.email = field("Email")

        self.type = ctk.CTkOptionMenu(container,
                                      values=["Property Management", "Landlord", "Other"])
        self.type.pack(pady=10)

        ctk.CTkButton(container, text="Save",
                      fg_color=ACCENT,
                      command=self.add_landlord).pack(pady=10)

        ctk.CTkButton(container, text="Back",
                      command=self.show_landlords).pack()

    def add_landlord(self):
        data = {
            "first_name": self.fname.get(),
            "last_name": self.lname.get(),
            "company_name": self.company.get(),
            "username": self.luser.get(),
            "password": self.lpass.get(),
            "phone_number": self.phone.get(),
            "account_type": self.type.get(),
            "secondary_email": self.email.get()
        }

        requests.post("http://127.0.0.1:5000/landlords", json=data)
        self.show_landlords()

    # ================= PROFILE =================
    def show_profile(self):
        self.set_title("Profile")
        self.clear()

        ctk.CTkLabel(self.content,
                     text=f"Logged in as: {self.username}",
                     font=("Segoe UI", 16)).pack(pady=20)

    def logout(self):
        self.master.show_login()


# ================= RUN =================
if __name__ == "__main__":
    app = App()
    app.mainloop()