from gpiozero import Button
from time import time, sleep


class Trigger():
    
    def __init__(self, 
                 button_pin, 
                 cooldown_time = .5,
                 trigger_callback_pressed = None, 
                 trigger_callback_released = None, 
                 debounce_time=0.5):

        self.cooldown_time = cooldown_time
        self.debounce_time = debounce_time
        self.button = Button(button_pin)
        self.button.when_pressed = self.on_pressed
        self.button.when_released = self.on_released
        self.trigger_callback_pressed = trigger_callback_pressed
        self.trigger_callback_released = trigger_callback_released
        self.debounce_timestamp = time()
    
    def on_pressed(self):
        if ((time() - self.debounce_timestamp) > self.debounce_time):
            print("Trigger: button pressed")
            self.debounce_timestamp = time()
            self.trigger_callback_pressed()

    def on_released(self):
        self.trigger_callback_released()