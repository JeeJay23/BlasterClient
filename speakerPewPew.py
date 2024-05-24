from gpiozero import PWMOutputDevice
from threading import Thread
from time import sleep

class Speaker():
    
    def __init__(self, 
                 button_pin):
        
        self.speaker = PWMOutputDevice(button_pin)
    
    def play_pewpew(self, duty_cycle=0.5, duration=1):
        
        start_freq = 500
        end_freq = 100
        steps = 50
        step_duration = duration / steps

        for i in range(steps):
            freq = start_freq - (start_freq - end_freq) * (i / steps)
            self.speaker.frequency = freq
            self.speaker.value = 0.5  # 50% duty cycle
            sleep(step_duration)
        
        self.speaker.value = 0  # Turn off the sound

    def play_pewpew_async(self, volume, duration):
        thread = Thread(target=self.play_pewpew, args=(volume, duration))
        thread.start()
        return thread