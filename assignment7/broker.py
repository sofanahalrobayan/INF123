from network import Listener, Handler, poll


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)

class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name] = self 
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            name = str(name)
            txt = str(txt)
            txt_list = txt.split(" ")
            should_print = True
            for word in txt_list:
                if "+" in word[0]:
                    if word[1:] not in subs.keys():
                        subs[word[1:]] = [names[name]]
                    else:
                        subs[word[1:]].append(names[name])
                    should_print = False

                elif "#" in word[0]:
                    if word[1:] in subs.keys():
                        for name, person in names.items():
                            if person in subs[word[1:]]:
                                broadcast({'speak': name, 'txt': txt})
                        should_print = False

                elif "-" in word[0]:
                    if word[1:] not in subs.keys() or names[name] not in subs.get(word[1:]):
                        pass
                    else:
                        subs[word[1:]].remove(names[name])
                    should_print = False

                elif "@" in word[0]:
                    if word[1:] in names.keys():
                        for name in names.keys():
                            if name == word[1:]:
                                broadcast({'speak': name, 'txt': txt})
                    should_print = False

                else:
                    continue
            if should_print:
                broadcast({'speak': name, 'txt': txt})


Listener(8888, MyHandler)
while 1:
    poll(0.05)