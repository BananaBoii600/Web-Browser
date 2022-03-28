from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

root = Tk()
root.title("Text Editor")
root.geometry("1200x710")

global open_status_name
open_status_name = False

global selected
selected = False

def New_file():
    text.delete("1.0", END)
    root.title("Opened New File - Text Editor")
    status_bar.config(text="New File        ")
    global open_status_name
    open_status_name = False

def open_file():
    text.delete("1.0", END)
    text_file = filedialog.askopenfilename(title="Open File", filetypes=[("Text Files", "*.txt")])
    
    if text_file:
            global open_status_name
            open_status_name = text_file

    name = text_file
    status_bar.config(text=f"{name}        ")
    root.title(f"{name} - Text Editor")

    text_file = open(text_file, 'r')
    text_file_content = text_file.read()
    text.insert(END, text_file_content)

    text_file.close

def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=[("Text Files", "*.txt")])
    if text_file:
        name = text_file
        status_bar.config(text=f"{name} Saved        ")
        root.title(f"{name} - Text Editor")

        text_file = open(text_file, "w")
        text_file.write(text.get(1.0, END))
        text_file.close()

def save_file():
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(text.get(1.0, END))
        text_file.close()
        status_bar.config(text=f'Saved {open_status_name}')
    else:
        save_as_file()

def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if text.selection_get():
            selected = text.selection_get()
            text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)

def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if text.selection_get():
        selected = text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)

def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)

def Bold():
    bold_font = font.Font(text, text.cget("font"))
    bold_font.configure(weight="bold")

    text.tag_configure("bold", font=bold_font)
    
    current_tags = text.tag_names("sel.first")

    if "bold" in current_tags:
        text.tag_remove("bold", "sel.first", "sel.last")
    else:
        text.tag_add("bold", "sel.first", "sel.last")

def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        text.config(bg=my_color)

def Italics():
    italics_font = font.Font(text, text.cget("font"))
    italics_font.configure(slant="italic")

    text.tag_configure("italic", font=italics_font)
    
    current_tags = text.tag_names("sel.first")

    if "italic" in current_tags:
        text.tag_remove("italic", "sel.first", "sel.last")
    else:
        text.tag_add("italic", "sel.first", "sel.last")

def text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=my_color)
        color_font = font.Font(text, text.cget("font"))
        color_font.configure()
        text.tag_configure("colored", font=color_font, foreground=my_color)
        current_tags = text.tag_names("sel.first")
        if "colored" in current_tags:
            text.tag_remove("colored", "sel.first", "sel.last")
        else:
            text.tag_add("colored", "sel.first", "sel.last")

def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        text.config(fg=my_color)

toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

frame = Frame(root)
frame.pack(pady=5)

text_scroll = Scrollbar(frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(frame, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)

text = Text(frame, width=98, height=25, font=("Helvetica", 16), selectbackground="gray", selectforeground="black", undo=True, yscrollcommand=text_scroll.set,xscrollcommand=hor_scroll.set, wrap="none")
text.pack()

text_scroll.config(command=text.yview)
hor_scroll.config(command=text.xview)

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=New_file)
file_menu.add_command(label="Open", command = open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command = lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste           ", command=lambda: paste_text(False), accelerator="(Ctrl+p)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo          ", command=text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=text.edit_redo, accelerator="(Ctrl+y)")

color_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Selected Text", command=text_color)
color_menu.add_command(label="All Text", command=all_text_color)
color_menu.add_command(label="Background", command=bg_color)

status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)

bold_button = Button(toolbar_frame, text="Bold", command=Bold)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

italics_button = Button(toolbar_frame, text="Italics", command=Italics)
italics_button.grid(row=0, column=1, padx=5)

undo_button = Button(toolbar_frame, text="Undo", command=text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text="Redo", command=text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

color_text_button = Button(toolbar_frame, text="Text Color", command=text_color)
color_text_button.grid(row=0, column=4, padx=5)

root.mainloop()