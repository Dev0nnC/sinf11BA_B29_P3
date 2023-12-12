# Imports go at the top
from microbit import *
import radio
radio.config(group=23)
radio.on()
connected = 0

# Code in a 'while True:' loop repeats forever
while True:
    display.show('% ' + str(connected) + '%')
    if connected == 0 or connected == 1:
        display.scroll('MWM')
        radio.send('C' + str(connected))
        radioR = radio.receive()
        if radioR:
            if radioR[1] == '0':
                display.show(Image.HAPPY)
                display.scroll('++')
                connected = 1
                radio.send('c1')
            elif radioR[1] == '1':
                display.show(Image.SMILE)
                display.scroll('---')
                connected == 2
                display.scroll(connected)
                radio.send('c2')
    elif connected == 2:
        display.scroll('*****')
        display.show(Image.HOUSE)
        sleep(5000)
                
            
        
    
