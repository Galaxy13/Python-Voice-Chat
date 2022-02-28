from tkinter import *
import client

def connect():
    client_obj = client.Client(text_ip.get(), text_port.get())
    client_obj.connect()
    if client_obj.connected:
        connection_status.configure(text='Connection successful')
        client_obj.client_launch()

window = Tk()
window.title('Voice chat для пацанов')
label = Label(window, text='Pre-alpha 2', font=("Times New Roman", 30))
window.geometry('300x150')
label.grid(column=0, row=0)
button_connect = Button(window, text='Connect to server', bg='pink', fg='black', command=connect)
button_connect.grid(column=1, row=0)

connection_status = Label(window, text='Not connected!', font=("Times New Roman", 15))
connection_status.grid(column=0, row=10)

text_ip = Entry(window, width=30)
text_port = Entry(window, width=10)

text_ip.grid(column=0, row=4)
text_port.grid(column=0, row=8, pady=10)

label_ip = Label(window, text='IP Address')
label_port = Label(window, text='Port')
label_ip.grid(column=1, row=4, padx=1)
label_port.grid(column=1, row=8, padx=1)

window.mainloop()