import random
from time import sleep
from common import Model
            
################### CONTROLLER #############################

class Controller():
    def __init__(self, m):
        self.m = m
    
    def poll(self):
        cmd = random.choice(self.m.cmd_directions.keys())
        if cmd:
            self.m.do_cmd(cmd)

################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        self._counter = 0
        
    def display(self):
        b = self.m.mybox
        self._counter += 1
        if self._counter == 50:
            print("Position: " + str(b[0]) + ", " + str(b[1]))
            self._counter = 0
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()