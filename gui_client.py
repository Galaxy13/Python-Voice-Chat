# Graphical interface for Audio client
from tkinter import *
from tkinter.ttk import Combobox
import client

client_obj = client.Client()
window = Tk()

SPK_IMAGE = PhotoImage(file=r"res\images\spk.png").subsample(10, 10)
SPK_IMAGE_OFF = PhotoImage(file=r"res\images\spk_off.png").subsample(10, 10)
MIC_IMAGE = PhotoImage(file=r"res\images\mic.png").subsample(10, 10)
MIC_IMAGE_OFF = PhotoImage(file=r"res\images\mic_off.png").subsample(10, 10)
CHAT_IMAGE = PhotoImage(file=r"res\images\chat.png").subsample(10, 10)

text = ''

MIC_TICK = False
SPK_TICK = False


def connect():
    """
    Initializing connection to server
    """
    client_obj.set_target_ip(text_ip.get())
    client_obj.set_port(text_port.get())
    client_obj.connect()
    if client_obj.connected:
        connection_status.configure(text='Connection successful')
        client_obj.client_launch()


def input_box():
    """
    Handler for input device
    Combobox
    :return:
    """
    input_obj = Combobox(window)
    input_obj['values'] = [device for device in client_obj.input_devices.keys()]
    input_obj.grid(column=2, row=0, padx=5)
    input_obj.current(input_obj['values'].index(client_obj.p.get_default_input_device_info().get('name')))
    input_obj.bind("<<ComboboxSelected>>", callbackIn)


def output_box():
    """
    Handler for output device
    Combobox
    :return:
    """
    output_obj = Combobox(window)
    output_obj['values'] = [device for device in client_obj.output_devices.keys()]
    output_obj.grid(column=2, row=1, padx=5)
    output_obj.current(output_obj['values'].index(client_obj.p.get_default_output_device_info().get('name')))
    output_obj.bind("<<ComboboxSelected>>", callbackOut)


def callbackIn(event):
    """
    Event handler for
    input Combobox
    :param event:
    :return:
    """
    device = client_obj.input_devices[event.widget.get()]
    client_obj.set_input_device(device)


def callbackOut(event):
    """
    Event handler for
    output Combobox
    :param event:
    :return:
    """
    device = client_obj.output_devices[event.widget.get()]
    client_obj.set_output_device(device)


def mic_control():
    """
    Mic control
    button initialize
    :return:
    """
    global mic_button
    mic_button = Button(window, image=MIC_IMAGE, command=mic_client_control)
    mic_button.image = MIC_IMAGE
    mic_button.place(x=320, y=100)


def spk_control():
    """
    Speaker control
    button initialize
    :return:
    """
    global spk_button
    spk_button = Button(window, image=SPK_IMAGE, command=spk_client_control)
    spk_button.image = SPK_IMAGE
    spk_button.place(x=400, y=100)


def mic_client_control():
    """
    Mic control
    handler
    :return:
    """
    global mic_button, MIC_TICK
    if not MIC_TICK:
        client_obj.input_stop()
        mic_button.configure(image=MIC_IMAGE_OFF)
        mic_button.image = MIC_IMAGE_OFF
        MIC_TICK = True
    else:
        client_obj.input_start()
        mic_button.configure(image=MIC_IMAGE)
        mic_button.image = MIC_IMAGE
        MIC_TICK = False


def spk_client_control():
    """
    Speaker control
    handler
    :return:
    """
    global spk_button, SPK_TICK
    if not SPK_TICK:
        client_obj.output_stop()
        spk_button.configure(image=SPK_IMAGE_OFF)
        spk_button.image = SPK_IMAGE_OFF
        SPK_TICK = True
    else:
        client_obj.output_start()
        spk_button.configure(image=SPK_IMAGE)
        spk_button.image = SPK_IMAGE
        SPK_TICK = False


def openNewWindow():
    global text_window
    chatWindow = Toplevel(window)

    chatWindow.title('Chat Window')

    chatWindow.geometry('400x800')

    Label(chatWindow, text='Chat Window').pack()

    text_window = Text(chatWindow)
    text_window.pack()

    chatWindow.mainloop()

def chat_open_button():
    chat_button = Button(window, image=CHAT_IMAGE, command=openNewWindow)
    chat_button.image = CHAT_IMAGE
    chat_button.place(x=360, y=160)


window.title('Voice chat для пацанов')
label = Label(window, text='Pre-alpha v5', font=("Times New Roman", 30))
window.geometry('460x250')
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

input_box()
output_box()
mic_control()
spk_control()
chat_open_button()
window.mainloop()
