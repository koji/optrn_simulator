import tkinter as tk
import requests
import uuid
# from utils import CustomText

def generate_unique_name():
    unique_name = str(uuid.uuid4()) + ".py"
    return unique_name

def send_post_request(payload):
    url = "https://baxin-simulator.hf.space/protocol"
    protocol_name = generate_unique_name()
    data = {"name": protocol_name, "content": payload}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        print("Error: " + response.text)
        return "Error: " + response.text

    # Check the response before returning it
    # ToDo clean up code
    response_data = response.json()
    if "error_message" in response_data:
        print("Error in response:", response_data["error_message"])
        return response_data["error_message"]
    elif "protocol_name" in response_data:
        # print("Protocol executed successfully. Run log:", response_data["run_log"])

        return response_data["run_status"]
        # ToDo if run_log option is on
        # return response_data["run_log"]
    else:
        print("Unexpected response:", response_data)
        return "Unexpected response"

def send_code(text):
   # Send POST request and get response
   response = send_post_request(text)
   # Update chatbot with response
   return response


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
text_box1.grid(row=0, column=0, sticky="nsew")

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, sticky="nsew")

# Create the 'Clear' button
clear_button = tk.Button(button_frame, text='Clear', command=clear_text)
clear_button.pack(side=tk.RIGHT)

# Create the 'Send' button
send_button = tk.Button(button_frame, text='Send', command=send_text)
send_button.pack(side=tk.RIGHT)

# Create the second text box
text_box2 = tk.Text(root)
text_box2.grid(row=2, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# menu config
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# Start the Tkinter event loop
root.mainloop()
