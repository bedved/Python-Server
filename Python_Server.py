import threading
import tkinter as tk
from tkinter import ttk
import http.server


def start_server(port):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    httpd.serve_forever()


def submit():
    console.delete('1.0', tk.END)
    port = int(port_entry.get())
    threading.Thread(target=start_server, args=(port,), daemon=True).start()
    submit_button.config(state="disabled")
    port_entry.config(state="disabled")




class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        custom_message = custom_message_entry.get()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(custom_message.encode())
        console.insert(tk.END, f"Received GET request and sent content: {custom_message}\n")
        console.see(tk.END)



    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        content = self.rfile.read(content_length).decode("utf-8")

        with open("log.txt", "a") as f:
            f.write(f"Content: {content}\n")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Data saved.")
        console.insert(tk.END, f"Received POST request with content: {content}\n")
        console.see(tk.END)



app = tk.Tk()
app.title("Hello World HTTP Server")
app.geometry("400x400")
app.resizable(True, True)

port_label = ttk.Label(app, text="Port:")
port_label.grid(column=0, row=0)
port_entry = ttk.Entry(app)
port_entry.grid(column=1, row=0)
port_entry.insert(0, "8080")

submit_button = ttk.Button(app, text="Start Server", command=submit)
submit_button.grid(column=0, row=1, columnspan=2)

console_label = ttk.Label(app, text="Console:")
console_label.grid(column=0, row=2)
console_scrollbar = ttk.Scrollbar(app)
console_scrollbar.grid(column=2, row=3, sticky="ns")
console = tk.Text(app, height=10, yscrollcommand=console_scrollbar.set)
console.grid(column=0, row=3, columnspan=2, sticky="nsew")
console_scrollbar.config(command=console.yview)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(3, weight=1)

custom_message_label = ttk.Label(app, text="Custom Message (GET):")
custom_message_label.grid(column=0, row=4)
custom_message_entry = ttk.Entry(app)
custom_message_entry.grid(column=1, row=4)
custom_message_entry.insert(0, "Hello World!")


app.mainloop()
