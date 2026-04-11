import tkinter as tk
from tkinter import messagebox

tasks = []
root = None
tasks_listbox = None
input_entry = None
input_label = None
current_input_callback = None


def create_main_window():
    global root

    root = tk.Tk()
    root.title("Tkinter Example")
    root.geometry("420x180")

    title_label = tk.Label(root, text="Tkinter is ready", font=("Arial", 14))
    title_label.pack(pady=16)

    info_label = tk.Label(
        root,
        text="If you can see this window, tkinter is installed and working.",
    )
    info_label.pack(pady=8)

    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)

    root.mainloop()

def main():
    create_main_window()

if __name__ == "__main__":
    main()