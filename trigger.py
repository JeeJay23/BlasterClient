from gpiozero import Button
from time import time, sleep


class Trigger():
    
    def __init__(self, 
                 button_pin, 
                 cooldown_time = .5,
                 trigger_callback_pressed = None, 
                 trigger_callback_released = None, 
                 debounce_time=0.05):

        self.cooldown_time = cooldown_time
        self.debounce_time = debounce_time
        self.button = Button(button_pin)
        self.button.when_pressed = self.on_pressed
        self.button.when_released = self.on_released
        self.trigger_callback_pressed = trigger_callback_pressed
        self.trigger_callback_released = trigger_callback_released
        self.cooldown_timestamp = time()
    
    def on_pressed(self):
        sleep(self.debounce_time)  # Debounce the signal
        if ((time() - self.cooldown_timestamp) > self.cooldown_time):
            self.cooldown_timestamp = time()
            # why are we checking this again?
            if self.button.is_pressed:
                self.trigger_callback_pressed()

    def on_released(self):
        self.trigger_callback_released()