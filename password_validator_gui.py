import tkinter as tk
from tkinter import messagebox
from password_validator import is_valid_password

class PasswordValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Validator App")
        self.root.geometry("420x560")
        self.root.resizable(True, True)

        # Main frame
        main_frame = tk.Frame(root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=18, pady=18)

        # Title and instructions
        tk.Label(main_frame, text="Password Validator", font=("Arial", 20, "bold"), bg="#f5f5f5").pack(pady=(10, 8))
        tk.Label(main_frame, text="Enter your password below:", font=("Arial", 12), bg="#f5f5f5").pack(pady=(0, 10))

        # Password entry
        entry_frame = tk.Frame(main_frame, bg="#f5f5f5")
        entry_frame.pack(pady=(0, 10))
        entry_border = tk.Frame(entry_frame, bg="#bdbdbd", highlightbackground="#bdbdbd", highlightthickness=1)
        entry_border.pack(side="left", padx=(0, 8))
        self.pwd_entry = tk.Entry(entry_border, show="*", width=28, font=("Arial", 14), relief="flat", bd=0, bg="#fff")
        self.pwd_entry.pack(ipady=6)

        # Show/hide password checkbox
        self.show_pwd_var = tk.BooleanVar()
        show_pwd_cb = tk.Checkbutton(entry_frame, text="Show", variable=self.show_pwd_var, command=self.toggle_password, bg="#f5f5f5", font=("Arial", 11))
        show_pwd_cb.pack(side="left")

        # Tooltip icon
        tooltip_icon = tk.Label(entry_frame, text="ⓘ", font=("Arial", 13), fg="#2196f3", bg="#f5f5f5")
        tooltip_icon.pack(side="left", padx=(8,0))
        tooltip_icon.bind("<Enter>", lambda e: self.show_tooltip())
        tooltip_icon.bind("<Leave>", lambda e: self.hide_tooltip())

        # Tooltip label
        self.tooltip = tk.Label(main_frame, text="Password must meet all requirements below.", font=("Arial", 10), bg="#fffde7", fg="#333", bd=1, relief="solid")
        self.tooltip.place_forget()

        # Requirements checklist
        self.requirements = [
            ("At least 8 characters", lambda pwd: len(pwd) >= 8),
            ("Contains uppercase letter", lambda pwd: any(c.isupper() for c in pwd)),
            ("Contains lowercase letter", lambda pwd: any(c.islower() for c in pwd)),
            ("Contains digit", lambda pwd: any(c.isdigit() for c in pwd)),
            ("Contains special character (!@#$%^&* etc.)", lambda pwd: any(c in '!@#$%^&*(),.?":{}|<>' for c in pwd)),
            ("No whitespace", lambda pwd: not any(c.isspace() for c in pwd)),
            ("Not a common password", lambda pwd: pwd not in {"password", "123456", "qwerty", "letmein", "admin", "iloveyou"}),
        ]
        self.req_labels = []
        req_frame = tk.Frame(main_frame, bg="#f5f5f5")
        req_frame.pack(pady=(8, 0))
        for text, _ in self.requirements:
            lbl = tk.Label(req_frame, text=f"✗ {text}", font=("Arial", 10), fg="#d32f2f", bg="#f5f5f5", anchor="w")
            lbl.pack(fill="x", padx=8, pady=1)
            self.req_labels.append(lbl)

        # Strength meter
        self.strength_var = tk.StringVar(value="")
        strength_frame = tk.Frame(main_frame, bg="#f5f5f5")
        strength_frame.pack(pady=(6, 0))
        self.strength_bar = tk.Canvas(strength_frame, width=260, height=18, bg="#e0e0e0", highlightthickness=0)
        self.strength_bar.pack(side="top", anchor="center")
        self.strength_label = tk.Label(strength_frame, textvariable=self.strength_var, font=("Arial", 10, "bold"), bg="#f5f5f5")
        self.strength_label.pack(side="top", pady=(0, 8), anchor="center")

        # Result label
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 15, "bold"), bg="#f5f5f5")
        self.result_label.pack(pady=(18, 18))

        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(pady=(0, 30), fill="x")
        btn_font = ("Arial", 14, "bold")
        btn_width = 12
        validate_btn = tk.Button(btn_frame, text="Validate", command=self.validate_password, font=btn_font, width=btn_width, bg="#388e3c", fg="white", relief="flat", bd=0)
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_fields, font=btn_font, width=btn_width, bg="#e0e0e0", relief="flat", bd=0)
        exit_btn = tk.Button(btn_frame, text="Exit", command=root.quit, font=btn_font, width=btn_width, bg="#f44336", fg="white", relief="flat", bd=0)
        validate_btn.grid(row=0, column=0, padx=(0, 12), sticky="ew")
        clear_btn.grid(row=0, column=1, padx=12, sticky="ew")
        exit_btn.grid(row=0, column=2, padx=(12,0), sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        # Bind real-time feedback
        self.pwd_entry.bind("<KeyRelease>", self.on_password_change)

    # --- Class methods ---
    def on_password_change(self, event=None):
        pwd = self.pwd_entry.get()
        for i, (text, check) in enumerate(self.requirements):
            if check(pwd):
                self.req_labels[i].config(text=f"✓ {text}", fg="#388e3c")
            else:
                self.req_labels[i].config(text=f"✗ {text}", fg="#d32f2f")
        score = sum(check(pwd) for _, check in self.requirements)
        if score <= 3:
            color, label = "#d32f2f", "Weak"
        elif score <= 5:
            color, label = "#fbc02d", "Medium"
        else:
            color, label = "#388e3c", "Strong"
        self.strength_bar.delete("all")
        self.strength_bar.create_rectangle(0, 0, score*37, 18, fill=color, outline="")
        self.strength_var.set(f"Password strength: {label}")
        self.result_label.config(text="")

    def toggle_password(self):
        if self.show_pwd_var.get():
            self.pwd_entry.config(show="")
        else:
            self.pwd_entry.config(show="*")

    def clear_fields(self):
        self.pwd_entry.delete(0, tk.END)
        self.result_label.config(text="", fg="black")
        for i, (text, _) in enumerate(self.requirements):
            self.req_labels[i].config(text=f"✗ {text}", fg="#d32f2f")
        self.strength_bar.delete("all")
        self.strength_var.set("")

    def validate_password(self):
        password = self.pwd_entry.get()
        if not password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return
        if is_valid_password(password):
            self.result_label.config(text=f"Accepted ✅\n{password}", fg="#388e3c")
        else:
            self.result_label.config(text=f"Rejected ❌\n{password}", fg="#d32f2f")

    def show_tooltip(self):
        self.tooltip.place(x=50, y=100)

    def hide_tooltip(self):
        self.tooltip.place_forget()


def main():
    root = tk.Tk()
    app = PasswordValidatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
