import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.length_entry = ttk.Entry(root, width=10)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)

        self.complexity_label = ttk.Label(root, text="Password Complexity:")
        self.complexity_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.complexity_combobox = ttk.Combobox(root, values=["Low", "Medium", "High"])
        self.complexity_combobox.current(1)
        self.complexity_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.exclude_label = ttk.Label(root, text="Exclude Characters:")
        self.exclude_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.exclude_entry = ttk.Entry(root, width=30)
        self.exclude_entry.grid(row=2, column=1, padx=5, pady=5)

        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def generate_password(self):
        length = self.length_entry.get()
        complexity = self.complexity_combobox.get()
        exclude_chars = self.exclude_entry.get()

        try:
            length = int(length)
            if length <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for password length.")
            return

        if complexity == "Low":
            characters = string.ascii_letters + string.digits
        elif complexity == "Medium":
            characters = string.ascii_letters + string.digits + string.punctuation
        else:  # High complexity
            characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_uppercase

        if exclude_chars:
            characters = ''.join(c for c in characters if c not in exclude_chars)

        password = ''.join(random.choice(characters) for _ in range(length))

        self.show_password_dialog(password)

    def show_password_dialog(self, password):
        dialog = tk.Toplevel(self.root)
        dialog.title("Generated Password")

        password_label = ttk.Label(dialog, text="Your Generated Password:")
        password_label.grid(row=0, column=0, padx=5, pady=5)

        password_entry = ttk.Entry(dialog, width=30)
        password_entry.grid(row=1, column=0, padx=5, pady=5)
        password_entry.insert(0, password)
        password_entry.configure(state='readonly')

        copy_button = ttk.Button(dialog, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(password))
        copy_button.grid(row=2, column=0, padx=5, pady=5)

    def copy_to_clipboard(self, password):
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()