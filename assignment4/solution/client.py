from network import Handler, poll
import sys
from threading import Thread


keep_going = True

myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
        print '**** Disconnected from server ****'
        global keep_going
        keep_going = False
        
    def on_msg(self, msg):
        if 'join' in msg:
            user_list = ','.join(msg['users'])
            print '%s joined. Users: %s' % (msg['join'], user_list)
        elif 'leave' in msg:
            user_list = ','.join(msg['users'])
            print '%s left the room. Users: %s' % (msg['leave'], user_list)
        elif 'speak' in msg and msg['speak'] != myname:
            print '%s: %s' % (msg['speak'], msg['txt'])
        

client = Client('localhost', 8888)
client.do_send({'join': myname})

def process_input():
    while keep_going:
        mytxt = sys.stdin.readline().rstrip()
        if mytxt == 'quit' or mytxt == 'exit':
            client.do_close()
        elif mytxt:  # ignore empty strings
            client.do_send({'speak': myname, 'txt': mytxt})
                            
thread = Thread(target=process_input)
thread.daemon = True  # die when the main thread dies 
thread.start()

while keep_going:
    poll(0.05)