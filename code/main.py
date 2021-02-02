from annieController import AnnieController
import PySimpleGUI as sg

annie = AnnieController()

recordIcon = '../icon.jpg'

sg.theme('DarkRed2')

layout = [[sg.Text("Press Record to Start Talking")], [sg.Button('Record')]]

# Create the window
window = sg.Window("Annie Virtual Assistant", layout)

# Create an event loop
while True:
    event, values = window.read()
    if event == "Record":
        annie.play()
    if event == sg.WIN_CLOSED:
        break
