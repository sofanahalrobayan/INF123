from random import choice, randint
from time import sleep
from network import Handler, poll

keep_going = True
da_model = None

################### MODEL ##################################
def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1

class Model(Handler):

    cmd_directions = {'up': (0, -1),
                      'down': (0, 1),
                      'left': (-1, 0),
                      'right': (1, 0)}

    def __init__(self):
        Handler.__init__(self,'localhost', 8888)
        self.borders = []
        self.pellets =  [[randint(10, 380), randint(10, 280), 5, 5] for _ in range(4) ]
        self.players = {}
        self.myname = None
        self.game_over = False
        self.mybox = [200, 150, 10, 10] 
        self.mydir = self.cmd_directions['down']

    def on_open(self):
        print '**** Connected to server ****'

    def on_close(self):
        global keep_going
        keep_going = False
        print '**** Disconnected from server ****'
        

    def do_cmd(self, cmd):
        if cmd == 'quit':
            self.game_over = True

        else:
            self.mydir = self.cmd_directions[cmd]

    def update(self):
        # move me
        self.mybox[0] += self.mydir[0]
        self.mybox[1] += self.mydir[1]
        # potential collision with a border
        for b in self.borders:
            if collide_boxes(self.mybox, b):
                self.mybox = [200, 150, 10, 10]
        # potential collision with a pellet
        for index, pellet in enumerate(self.pellets):
            if collide_boxes(self.mybox, pellet):
                self.mybox[2] *= 1.2
                self.mybox[3] *= 1.2
                self.pellets[index] = [randint(10, 380), randint(10, 280), 5, 5]



################### NETWORK CONTROLLER #############################

class NetworkController():

    def __init__(self, m):
        self.m = m

    def poll(self):
        p = self.m.pellets[0] 
        
        b = self.m.mybox
        if p[0] > b[0]:
            cmd = 'right'
        elif p[0] < b[0]:
            cmd = 'left'
        elif p[1] > b[1]:
            cmd = 'down'
        else:
            cmd = 'up'
        self.m.do_cmd(cmd)


        
################### CONSOLE VIEW #############################

class ConsoleView():
    def __init__(self, m):
        self.m = m
        self.frame_freq = 20
        self.frame_count = 0
        self._prev_x = self.m.mybox[2]
        self._prev_y = self.m.mybox[3]
        
    def display(self):
        if self.m.mybox[2] > self._prev_x or self.m.mybox[3] > self._prev_y:
            self._prev_x = self.m.mybox[2]
            self._prev_y = self.m.mybox[3]
            print 'Ate a pellet'
        
        
################### LOOP #############################

model = Model()
c = NetworkController(model)
v = ConsoleView(model)

while not model.game_over and keep_going:
    sleep(0.02)
    poll()
    c.poll()
    model.update()
    v.display()