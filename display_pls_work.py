from rpi_lcd import LCD

class Display():

    def __init__(self, name="Sjaakie", score=0):
        self.lcd = LCD()
        self.name = name
        self.score = score
        self.hit = False
        self.update_display()

    ## TODO update_score needs a parameter 'score' to update the score to the score the server replies back
    def update_score(self):
        self.score = self.score + 1
        #self.score = score
        self.update_display()

    def update_name(self, name):
        self.name = name
        self.update_display()

    def update_display(self):
        self.lcd.text(self.name, 1)
        line_2_text = "Score: {}{}".format(self.score, " - Hit!" if self.hit else "")
        self.lcd.text(line_2_text, 2)

    def clear_display(self):
        self.lcd.clear()