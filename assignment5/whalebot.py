import random
from time import sleep
from common import Model
            
################### CONTROLLER #############################

class Controller():
    def __init__(self, m):
        self.m = m
    
    def poll(self):
        #----------------- Question 2 ---------------------
        # cmd = random.choice(self.m.cmd_directions.keys())
        # if cmd:
        #     self.m.do_cmd(cmd)
        for i in self.m.pellets:
            pellet_x = i[0]
            pellet_y = i[1]
            my_box_x = self.m.mybox[0]
            my_box_y = self.m.mybox[1]

            if my_box_x < pellet_x:
                self.m.do_cmd('right')
            elif my_box_y > pellet_y:
                self.m.do_cmd('up')
            elif my_box_y < pellet_y:
                self.m.do_cmd('down')
            elif my_box_x > pellet_x:
                self.m.do_cmd('left')


################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        self._frame = 0
        
    def display(self):
        da_box = self.m.mybox
        self._frame += 1

        if self._frame == 50:
            print("Position: " + str(da_box[0]) + ", " + str(da_box[1]))
            self._frame = 0
    
################### LOOP #############################
import whaleuser
model = Model()
c = Controller(model)
v = whaleuser.View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()