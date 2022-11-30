from yui import Buzzer, RGB
import time
import board
from random import randint

max_trials = 3
trials = 0

RT = []
Word = []
Color = []

bt1 = Buzzer(pins = board.GP20)
bt1.connect()
bt2 = Buzzer(pins = board.GP21)
bt2.connect()
bt3 = Buzzer(pins = board.GP22)
bt3.connect()
rgb = RGB()
rgb.connect()

State = "Welcome"
rgb.white()
print("Welcome participant")

def create_csv(word, color, rt):
    n_obs = len(rt)
    output = "Color, Word, RT\n"
    for row in range(0, n_obs):
        this_row = color[row] + "," + word[row] + "," + str(rt[row]) + "\n"
        output = output + this_row        
    return output

while True:
    now = time.monotonic()
    if State == "Welcome" and bt1.update() and bt1.value:
        State = "Fixation"
        ts_fixation = now
        print("X")
    elif State == "Fixation" and now - ts_fixation > 0.5:
        State = "Stimulus"
        trials += 1
        if randint(0,1):
            this_word = "red"
        else:
            this_word = "green"
        if randint(0,1):
            this_color = "red"
            rgb.red()
        else:
            this_color = "green"
            rgb.green()
        print(this_word)
        ts_RT = now
            
    elif State == "Stimulus" and (bt2.update() and bt2.value) or (bt3.update() and bt3.value):
        State = "Feedback"
        this_RT = now - ts_RT
        RT.append(this_RT)
        Color.append(this_color)
        Word.append(this_word)
        print(this_word + "-" + this_color + ":" + str(this_RT))
    elif State == "Feedback" and (bt1.update() and bt1.value):
        if trials == max_trials:
            State = "Goodbye"
            results = create_csv(Word, Color, RT)
            print(results)
        else:
            State = "Fixation"
            ts_fixation = now
        
