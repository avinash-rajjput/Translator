from tkinter import *
from tkinter import ttk
from deep_translator import GoogleTranslator
import pyperclip
import threading
import time
import winsound  # For sound effects

def change(text="type", src="english", dest="hindi"):
    try:
        translated_text = GoogleTranslator(source=src, target=dest).translate(text)
        return translated_text
    except Exception as e:
        return "Error: Translation Failed"

def data():
    s = comb_sor.get()
    d = comb_dest.get()
    masg = Sor_txt.get(1.0, END).strip()
    
    # Show progress bar
    progress_bar.place(x=100, y=400, width=300)
    progress_bar.start()
    root.update()
    
    def translate():
        textget = change(text=masg, src=s, dest=d)
        progress_bar.stop()
        progress_bar.place_forget()
        dest_txt.delete(1.0, END)
        dest_txt.insert(END, textget)
        fade_in(dest_txt)
        winsound.Beep(1000, 200)  # Play a sound when translation is complete
    
    threading.Thread(target=translate).start()

def fade_in(widget):
    for i in range(10):
        widget.configure(fg=f"#{i*25:02x}{i*25:02x}{i*25:02x}")
        root.update()
        time.sleep(0.02)
    widget.configure(fg="black")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#2E2E2E" if dark_mode else "#E6F3FF"  # Light blue in light mode
    fg_color = "white" if dark_mode else "black"
    btn_color = "#555" if dark_mode else "SystemButtonFace"
    
    root.configure(bg=bg_color)
    label_title.configure(bg=bg_color, fg=fg_color)
    label_source.configure(bg=bg_color, fg=fg_color)
    label_dest.configure(bg=bg_color, fg=fg_color)
    dark_mode_btn.configure(bg=btn_color, fg=fg_color)
    
    Sor_txt.configure(bg="#FFFFFF" if dark_mode else "white", fg="black")
    dest_txt.configure(bg="#FFFFFF" if dark_mode else "white", fg="black")
    
    # Smooth transition
    for i in range(10):
        root.update()
        time.sleep(0.02)

def copy_to_clipboard():
    text = dest_txt.get(1.0, END).strip()
    pyperclip.copy(text)
    show_tooltip(copy_btn, "Copied!")

def clear_text():
    Sor_txt.delete(1.0, END)
    dest_txt.delete(1.0, END)

def detect_language():
    text = Sor_txt.get(1.0, END).strip()
    if text:
        detected_lang = GoogleTranslator().detect(text)
        comb_sor.set(detected_lang)
        show_tooltip(detect_btn, f"Detected: {detected_lang}")

def show_tooltip(widget, text):
    tooltip = Label(root, text=text, bg="yellow", fg="black", font=("Arial", 10))
    tooltip.place(x=widget.winfo_x(), y=widget.winfo_y() - 20)
    root.after(2000, tooltip.destroy)

def on_focus_in(widget):
    widget.configure(bg="#E0F7FA")

def on_focus_out(widget):
    widget.configure(bg="white")

root = Tk()
root.geometry('500x700')
root.title("Language Translator")
root.resizable(0,0)
root.configure(bg='#E6F3FF')  # Light blue background

dark_mode = False  # Track dark mode state

label_title = Label(root, text='Translator', font=("Times New Roman", 30, "bold"), bg="#E6F3FF", fg="black")
label_title.place(x=100, y=20, height=50, width=300)

dark_mode_btn = Button(root, text="Dark Mode", command=toggle_dark_mode)
dark_mode_btn.place(x=400, y=20, height=30, width=80)

label_source = Label(root, text='Source Text', font=("Times New Roman", 20, "bold"), fg="Black", bg="#E6F3FF")
label_source.place(x=100, y=80, height=30, width=300)

Sor_txt = Text(root, font=("Times New Roman", 16), wrap=WORD, bg="white", fg="black")
Sor_txt.place(x=10, y=120, height=100, width=480)
Sor_txt.bind("<FocusIn>", lambda e: on_focus_in(Sor_txt))
Sor_txt.bind("<FocusOut>", lambda e: on_focus_out(Sor_txt))

list_text = GoogleTranslator().get_supported_languages()
comb_sor = ttk.Combobox(root, value=list_text)
comb_sor.place(x=10, y=250, height=40, width=150)
comb_sor.set("english")

Button(root, text="Translate", relief=RAISED, command=data).place(x=170, y=250, height=40, width=150)

comb_dest = ttk.Combobox(root, value=list_text)
comb_dest.place(x=330, y=250, height=40, width=150)
comb_dest.set("hindi")

label_dest = Label(root, text='Translated Text', font=("Times New Roman", 20, "bold"), fg="Black", bg="#E6F3FF")
label_dest.place(x=100, y=310, height=30, width=300)

dest_txt = Text(root, font=("Times New Roman", 16), wrap=WORD, bg="white", fg="black")
dest_txt.place(x=10, y=350, height=150, width=480)
dest_txt.bind("<FocusIn>", lambda e: on_focus_in(dest_txt))
dest_txt.bind("<FocusOut>", lambda e: on_focus_out(dest_txt))

# Progress bar for translation
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, mode='indeterminate')

# Copy to clipboard button
copy_btn = Button(root, text="Copy", command=copy_to_clipboard)
copy_btn.place(x=10, y=520, height=30, width=80)

# Clear text button
clear_btn = Button(root, text="Clear", command=clear_text)
clear_btn.place(x=100, y=520, height=30, width=80)

# Detect language button
detect_btn = Button(root, text="Detect Language", command=detect_language)
detect_btn.place(x=190, y=520, height=30, width=120)

root.mainloop()