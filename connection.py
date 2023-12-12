# Imports go at the top
from microbit import *
import radio
radio.config(group=23)
radio.on()
connected = '0'

# Code in a 'while True:' loop repeats forever
while connected != '2':
    #sleep(500)
    display.show('% ' + connected + '%')
    #sleep(500)
    msgToSend = connected
    radio.send(msgToSend)
    radioR = radio.receive()
    if radioR:
        messageRecu = radioR
        #display.scroll('RECU' + messageRecu)
        if messageRecu == '0':
            #display.scroll('++')
            connected = '1'
            #display.scroll(connected + '**')
        else:
            connected = '2'
            #display.scroll('--' + connected + '~-')
            radio.send('2')
while True:
    display.show(Image.HOUSE)
