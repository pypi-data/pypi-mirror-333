#!/usr/bin/python

import io
import subprocess
import time
import atexit
import tkinter as tk
from PIL import Image
import os
from local_zebra_printer.socket_listener import SocketThread
from local_zebra_printer.zpl_methods import *

def xclip_exists():
    """Check if xclip is installed"""
    p = os.popen("which xclip")
    result = p.read().strip()
    return result



class ZebraPrinterGUI:
    def __init__(self, default_height="150", default_widht="100", default_zpl=DEFAULT_LABELARY_ZPL):
        self.root = tk.Tk()
        self.root.title("Zpl Printer")
        self.root.grid_rowconfigure(2, weight=1)
        for i in range(1, 5):
            self.root.grid_columnconfigure(i, weight=1)
        self.image = tk.PhotoImage()
        self.imagelabel = tk.Label(image=self.image)
        self.imagelabel.grid(row=2, column=1, columnspan=5, sticky="nsew")
        self.raw_image_data = bytes()
        if xclip_exists():
            B = tk.Button(self.root, text="Copy", command=self.copy_raw_image_to_clipboard)
            B.grid(row=1, column=1)
        else:
            B = tk.Button(
                self.root,
                text="No xclip",
                command=lambda: print("This button requires xclip to function. Install xclip and restart the program."),
            )
            B.grid(row=1, column=1)
        height_label = tk.Label(self.root, text="Height:")
        height_label.grid(row=1, column=2)
        self.height = tk.Entry(self.root)
        self.height.insert(0, default_height)
        self.height.grid(row=1, column=3)
        width_label = tk.Label(self.root, text="Width:")
        width_label.grid(row=1, column=4)
        self.width = tk.Entry(self.root)
        self.width.insert(0, default_widht)
        self.width.grid(row=1, column=5)
        self.zpl_text = tk.Text(self.root)
        self.zpl_text.grid(row=2, column=6, columnspan=5, sticky="nsew")
        self.zpl_text.insert(tk.END, default_zpl)
        self.prettify = tk.BooleanVar()
        prettify_checkbox = tk.Checkbutton(
            text="Prettify",
            variable=self.prettify,
            onvalue=True,
            offvalue=False,
            command=self.prettify_current,
        )
        prettify_checkbox.grid(row=1, column=7)

        send_button = tk.Button(self.root, text="Send", command=self.manual_upload)
        send_button.grid(row=1, column=6)
        self.zebra_socket = SocketThread(self.call_back_method)

    def show_image(self, raw_image: bytes):
        self.image.blank()
        time.sleep(0.1)
        pil_image = Image.open(io.BytesIO(raw_image))
        label_width = self.imagelabel.winfo_width()
        label_height = self.imagelabel.winfo_height()
        aspect_ratio = pil_image.width / pil_image.height

        # Calculate the new dimensions based on the aspect ratio
        if label_width / label_height > aspect_ratio:
            new_width = int(label_height * aspect_ratio)
            new_height = label_height
        else:
            new_width = label_width
            new_height = int(label_width / aspect_ratio)

        pil_image = pil_image.resize((new_width, new_height))
        output = io.BytesIO()
        pil_image.save(output, format="PNG")
        self.image.configure(data=output.getvalue(), format="png")
        self.raw_image_data = raw_image
        self.imagelabel.winfo_toplevel().attributes("-alpha", 0.5)

        self.imagelabel.winfo_toplevel().attributes("-alpha", 1)

    def copy_raw_image_to_clipboard(self):
        # Use the subprocess module to run the xclip command
        # and open a pipe to its standard input
        p = subprocess.Popen(
            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'],
            stdin=subprocess.PIPE,
        )

        # Write the raw bytes of the image to the standard input of the xclip process
        p.stdin.write(self.raw_image_data)

        # Close the pipe to the standard input of the xclip process
        p.stdin.close()

        # Wait for the xclip process to finish
        p.wait()


    def manual_upload(self):
        image_result = get_zpl_image_via_api(
            self.zpl_text.get(1.0,tk.END),
            int(self.height.get()),
            int(self.width.get()),
        )
        self.show_image(image_result.data)

    def prettify_current(self):
        zpl_code = self.zpl_text.get(1.0, tk.END)
        zpl_code = prettify_zpl_code(zpl_code)
        self.zpl_text.delete(1.0, tk.END)
        self.zpl_text.insert(tk.END, zpl_code)

    def call_back_method(self, connector, zpl_code):
        response = get_zpl_image_via_api(
            zpl_code, int(self.height.get()), int(self.width.get())
        )
        if response:
            self.show_image(response.data)
        self.zpl_text.delete(1.0, tk.END)
        if self.prettify.get():
            zpl_code = prettify_zpl_code(zpl_code)
        self.zpl_text.insert(tk.END, zpl_code)

    def on_closing_callback(self):
        self.zebra_socket.stop()
        self.root.destroy()

    def start(self):
        self.zebra_socket.daemon = True
        self.zebra_socket.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_callback)
        self.root.mainloop()


def main():
    gui = ZebraPrinterGUI()
    def unexpected_exit():
        try:
            gui.on_closing_callback()
        except Exception:
            return
    atexit.register(unexpected_exit)
    gui.start()


if __name__ == "__main__":
    main()