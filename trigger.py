from gpiozero import Button
from time import sleep

class Trigger():
    
    def __init__(self, button_pin, trigger_callback_pressed, trigger_callback_released, debounce_time=0.05):
        self.button_pin = button_pin
        self.debounce_time = debounce_time
        self.button = Button(self.button_pin)
        self.button.when_pressed = self.on_pressed
        self.button.when_released = self.on_released
        self.trigger_callback_pressed = trigger_callback_pressed
        self.trigger_callback_released = trigger_callback_released
    
    def on_pressed(self):
        sleep(self.debounce_time)  # Debounce the signal
        if self.button.is_pressed:
            self.trigger_callback_pressed()
            print('Button pressed wooo')

    def on_released(self):
        self.trigger_callback_released()
        print('Button released wooo')