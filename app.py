from tkinter import *
import tkinter.ttk as ttk
from serial import *
import serial.tools.list_ports
import re

root = Tk()
root.title("8 to 1 mux controler")

# initialization and open the port
ser_ = serial.Serial()
ser_.baudrate = 115200
# ser_.xonxoff = False  # disable software flow control
# ser_.rtscts = False  # disable hardware (RTS/CTS) flow control
# ser_.dsrdtr = False  # disable hardware (DSR/DTR) flow control


def remove_control_characters(s):
    regex = re.compile(r'[\r\t]')
    return regex.sub(" ", s)


def serial_ports():
    ports = serial.tools.list_ports.comports()
    ports_names = []
    ports_cb['values'] = ports_names

    if len(ports) > 0:
        for port in sorted(ports):
            print("{}".format(port.device))
            ports_names.append(port.device)
        ports_cb['values'] = ports_names
        ports_cb.current(0)


def on_select(event=None):
    # or get selection directly from combobox
    print("comboboxes: ", ports_cb.get())


def connect():
    global ser_
    ser_.close()
    ser_.port = ports_cb.get()
    try:
        ser_.open()
    except Exception:
        print("error open serial port")
    if ser_.isOpen():
        connectBtn.configure(state="disable", text="Connected", bg="green")


def sendCommand(cmd):
    ser_.write(cmd.encode("utf-8"))
    # putOnRecivebox(cmd)


def readSerial():
    try:
        if ser_.isOpen():
            if ser_.inWaiting() > 0:
                ser_bytes = ser_.readline()
                decoded_bytes = ser_bytes.decode("utf-8")
                putOnRecivebox(decoded_bytes)
    except:
        connectBtn.configure(state="normal", text="Connect", bg="red")


def putOnRecivebox(s):
    reciveBox.insert(END, remove_control_characters(s))
    reciveBox.see(END)


def sendOnEnter(event):
    sendCommand(sendBox.get()+"\r\n")
    sendBox.delete(0, END)


def setMux(btn):
    if(btn == 'CLOSE\rALL'):
        sendCommand("0\r\n")
    else:
        sendCommand(btn + "\r\n")

# define widgets
root.bind('<Return>', sendOnEnter)

ports_cb = ttk.Combobox(root, state="readonly")
ports_cb.bind('<<ComboboxSelected>>', on_select)

connectBtn = Button(root, text="Connect", width=20, pady=10,
                    command=connect)
rescanBtn = Button(root, text="Rescan Ports", width=20, pady=10,
                   command=serial_ports)

actionLab = Label(root,  text="Actions:", font="Arial 12 bold")

volumeLab = Label(root,  text="Action Volume (mL)", font="Arial 12 bold")
volume = Entry(root, font="Arial 12 bold", width=10, bg="blue", fg="white")

def numpad_create(self):

    btn_list = ['1','2','3','4','5','6','7','8','CLOSE\rALL']
    c = 0
    for b in btn_list:
            self.b = Button(self, text=b, width=3 ,height=3, bg='blue', fg="#FFFFFF", font=('bold',16),
                    activebackground='red', activeforeground="#FFFFFF", command = lambda btn=b:setMux(btn))
            self.b.grid(row=2,column=c)
            c += 1


sendBox = Entry(root, font="Arial 12 bold", width=80, bg="blue", fg="white")
reciveBox = Text(root, font="Arial 12 bold", width=80, height=30)


# order widgets
connectBtn.grid(row=1, column=6,columnspan=3)
ports_cb.grid(row=1, column=3,columnspan=3)
rescanBtn.grid(row=1, column=0,columnspan=3)

# sendBox.grid(row=9, column=0, columnspan=9)
# reciveBox.grid(row=10, column=0, columnspan=9)

serial_ports()
numpad_create(root)

while True:
    root.update_idletasks()
    root.update()
    # readSerial()
