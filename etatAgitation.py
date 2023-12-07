def on_button_pressed_a():
    basic.show_string("B")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    basic.show_string("AB")
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    basic.show_string("")
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_gesture_shake():
    if input.acceleration(Dimension.STRENGTH) <= 1000:
        basic.show_icon(IconNames.SMALL_DIAMOND)
        radio.send_value("shakeStrength", 0)
    elif input.acceleration(Dimension.STRENGTH) > 1000 or input.acceleration(Dimension.STRENGTH) <= 1300:
        basic.show_icon(IconNames.SQUARE)
        radio.send_value("shakeStrength", 1)
    elif input.acceleration(Dimension.STRENGTH) > 1300:
        basic.show_icon(IconNames.SMALL_HEART)
        radio.send_value("shakeStrength", 2)
    else:
        radio.send_value("shakeStrength", 3)
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

radio.set_group(1)

def on_forever():
    basic.show_icon(IconNames.HOUSE)
basic.forever(on_forever)
