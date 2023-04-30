import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Treeview demo')
root.geometry('620x200')

# define columns
columns = ('first_name', 'last_name', 'email', 'age')


tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
tree.heading('first_name', text='Primeiro Nome')
tree.pack()


root.mainloop()