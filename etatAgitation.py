from microbit import *
shakeStrength = 0

def on_gesture_shake():
    global shakeStrength
    shakeStrength = input.acceleration(Dimension.STRENGTH)
    if shakeStrength < 800:
        radio.send_value("shakeStrengthState", 0)
    elif shakeStrength >= 1000 and shakeStrength < 2000:
        radio.send_value("shakeStrengthState", 1)
    elif shakeStrength >= 2000:
        radio.send_value("shakeStrengthState", 2)
    else:
        basic.show_icon(IconNames.NO)
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def on_forever():
    global shakeStrength
    basic.show_string("B")
    shakeStrength = 0
    radio.set_group(1)
basic.forever(on_forever)
