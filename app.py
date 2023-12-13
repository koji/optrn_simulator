import tkinter as tk
from tklinenums import TkLineNumbers
from utils import send_code

def clear_text():
    # Clear the text boxes
    text_box1.delete('1.0', tk.END)
    text_box2.delete('1.0', tk.END)

def send_text():
    # Clear the text in text_box2
    text_box2.delete('1.0', tk.END)
    # Immediately update the GUI
    root.update_idletasks()

    # Get the text from text box 1
    code = text_box1.get('1.0', tk.END)

    response = send_code(code)

    text_box2.insert(tk.END, response)

# Create the main window
root = tk.Tk()
root.title("Opentrons Simulator UI")

# add menubar
menubar = tk.Menu(master=root)

# add file menu
filemenu = tk.Menu(master=menubar, tearoff=0)
filemenu.add_command(label="Quit", command=root.quit)

# text_box = Example(root)
# Create the first text box
text_box1 = tk.Text(root)
text_box1.grid(row=0, column=1, sticky="nsew")

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=1, sticky="nsew")

# Create the 'Clear' button
clear_button = tk.Button(button_frame, text='Clear', command=clear_text)
clear_button.pack(side=tk.RIGHT)

# Create the 'Send' button
send_button = tk.Button(button_frame, text='Send', command=send_text)
send_button.pack(side=tk.RIGHT)

# Create the second text box
text_box2 = tk.Text(root)
text_box2.grid(row=2, column=0, sticky="nsew", columnspan=2)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(1, weight=1)

# menu config
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


# tklinenums
linenums = TkLineNumbers(root, text_box1, justify="left", colors=("#2197db", "#ffffff"))
linenums.grid(row=0, column=0, sticky="nsew")
text_box1.bind("<<Modified>>", lambda event: root.after_idle(linenums.redraw), add=True)

# Start the Tkinter event loop
root.mainloop()
