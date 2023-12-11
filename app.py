import tkinter as tk
import uuid
from simulator import Simulator

protocol_simulator = Simulator()

def generate_unique_name():
    unique_name = str(uuid.uuid4()) + ".py"
    return unique_name

def send_post_request(payload):
    protocol_name = generate_unique_name()
    protocol = protocol_simulator.Protocol(name=protocol_name, content=payload)
    response_data = protocol_simulator.upload_protocol(protocol)
    
    #print(response_data)

    if "error_message" in response_data:
        print("Error in response:", response_data["error_message"])
        return response_data["error_message"]
    elif "protocol_name" in response_data:
        # print("Protocol executed successfully. Run log:", response_data["run_log"])

        return response_data["run_log"]
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
    # Get the text from text box 1
    code = text_box1.get('1.0', tk.END)
    
    response = send_code(code)
    
    text_box2.insert(tk.END, response)

# application part
# Create the main window
root = tk.Tk()

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

# Start the Tkinter event loop
root.mainloop()
