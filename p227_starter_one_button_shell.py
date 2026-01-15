import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import StringVar, filedialog
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
import platform

def do_command(command):
    # If url_entry is blank, use localhost IP address 
    url_val = url_entry.get()
    if (len(url_val) == 0):
        url_val = "127.0.0.1"
        # ::1 does not work on Mac, likely due to firewall settings
    
    command_textbox.delete(1.0, tk.END)
    command_textbox.insert(tk.END, command + " working....\n")
    command_textbox.update()

    command_list = command + " " + url_val
    #If running on Mac, replace commands where necessary
    if (platform.system() == "Darwin"):
        if (command == "tracert"):
            command = "traceroute"
        if (command == "ping"):
            command = "ping -c4" # Mac otherwise pings without limit
    
    # NOTE: For Mac, to avoid FileNotFoundError, create list of command args. (Alternative?: add shell=true option to Popen method call)
    command_list = (command + ' ' + url_val).split()
    
    """
    The following version of the subprocess failed to capture the first line of the command output
    (because not actually line buffering, because the PIPE is not a TTY; the stdout iteration starts too late):  
        subprocess.Popen(commandList, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)    
    """
    # These lines allow for real time output in the GUI
    with subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, text=True) as p:
        for line in p.stdout:
            command_textbox.insert(tk.END,line)
            command_textbox.update()
            
            
#add to main command
def do_comman(ipconfig):
    global url_val
    url_val = url_entry.get()
    with subprocess.Popen(ipconfig + ' ' + url_val, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            command_textbox.insert(tk.END,line)
            command_textbox.update()
    if (len(url_val) == 0):
        # url_val = "127.0.0.1"
        url_val = "::1"

    
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

# set up button to run the do_command function
ping_btn = tk.Button(frame, text="ping", command=do_command)
ping_btn.pack()

# creates the frame with label for the text box
frame_URL = tk.Frame(root, pady=10,  bg="black") # change frame color
frame_URL.pack()

# decorative label
url_label = tk.Label(frame_URL, text="Enter a URL of interest: ", 
    compound="center",
    font=("comic sans", 14),
    bd=0, 
    relief=tk.FLAT, 
    cursor="heart",
    fg="mediumpurple3",
    bg="black")
url_label.pack(side=tk.LEFT)
url_entry= tk.Entry(frame_URL,  font=("comic sans", 14)) # change font
url_entry.pack(side=tk.LEFT)

frame = tk.Frame(root,  bg="black") # change frame color
frame.pack()


# CODE TO ADD
# Save function.
def mSave():
  filename = asksaveasfilename(defaultextension='.txt',filetypes = (('Text files', '*.txt'),('Python files', '*.py *.pyw'),('All files', '*.*')))
  if filename is None:
    return
  file = open (filename, mode = 'w')
  text_to_save = command_textbox.get("1.0", tk.END)
  
  file.write(text_to_save)
  file.close()
  
save_btn = tk.Button(frame, text="save", command=mSave)
save_btn.pack()

# Adds an output box to GUI.
command_textbox = tksc.ScrolledText(frame, height=10, width=100)
command_textbox.pack()

# CODE TO ADD
# Makes the command button pass it's name to a function using lambda
ping_btn = tk.Button(frame, text="Check to see if a URL is up and active", command=lambda:do_command("ping"))
ping_btn.pack()


#ipconfig
ipconfig_setting = print("selit")
def ipconfig_runner():
    print(ipconfig_setting)
def ipconfig_setting_gelit():
    ipconfig_setting = print("gelit")
ipconfig_button = tk.Button(frame, text="ipconfig", command=lambda:ipconfig_runner(ipconfig_setting))
ipconfig_button.pack()
ipconfig_dropdown_list_var = StringVar(value="ipconfig")
ipconfig_dropdown = ttk.Combobox(root, textvariable= ipconfig_dropdown_list_var)
ipconfig_dropdown['values'] = ("gelit", "gelit squared", "gelit gah")
ipconfig_dropdown.state(["readonly"])
ipconfig_dropdown.bind('gelit', ipconfig_setting_gelit)

ipconfig_dropdown.pack()


root.mainloop()
