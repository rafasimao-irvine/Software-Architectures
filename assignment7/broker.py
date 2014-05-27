
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
            
            # Gets the text and split it to get the commands
            text = msg['txt']
            splitted_text = text.split(' ')
            is_subscribe = False
            
            # Subscribe command
            if '+' in msg['txt']:
                # Search for subscribes
                for txt in splitted_text:
                    if txt.__len__() > 0:
                        if '+' == txt[0]: # is subscribe?
                            is_subscribe = True
                            tag = txt[1:] # get the tag
                            # Adds the handler to the tag subscribers
                            if tag in subs:
                                handlers_list = subs[tag]
                                # Add handler if it isn't already there
                                if not self in handlers_list:
                                    handlers_list.append(self)
                            # If the tag didn't exist yet, creates it
                            else:
                                handlers_list = list()
                                handlers_list.append(self)
                                subs[tag] = handlers_list
            
            # Unsubscribe command
            if '-' in msg['txt']:
                # Search for subscribes
                for txt in splitted_text:
                    if txt.__len__() > 0:
                        if '-' == txt[0]: # is unsubscribe?
                            is_subscribe = True
                            tag = txt[1:] # get the tag
                            if tag in subs:
                                # unsubscrbes itself from the tag
                                if self in subs[tag]:
                                    subs[tag].remove(self)
                                    # remove the tag if there isnt anybody subscribed
                                    if subs[tag].__len__() < 1:
                                        del subs[tag]

            
            # Publish command(private and group)
            if '@' in msg['txt'] or '#' in msg['txt']:
                handlers_list = list() # inits handlers list
                # Search for tags to publish
                for txt in splitted_text:
                    if txt.__len__() > 0:
                        # group messages
                        if '#' == txt[0]: # is publish?
                            tag = txt[1:] # gets the tag
                            if tag in subs:
                                for h in subs[tag]:
                                    if not h in handlers_list: # is it already in the list?
                                        handlers_list.append(h) # add the handler to the list
                        # private messages
                        if '@' == txt[0]:
                            name = txt[1:]
                            if name in names: # add to the list if it is into the names list
                                if not names[name] in handlers_list:
                                    handlers_list.append(names[name])
                # Sends the msg to all the handlers in the list
                for h in handlers_list:
                    h.do_send(msg)
                        
            # If it is a general speak, broadcast it to everybody
            else:
                # Doesnt send to everybody only if it is a subscribe command
                if not is_subscribe:
                    broadcast({'speak': name, 'txt': txt})
            
            #print str(subs)
            



Listener(8888, MyHandler)
while 1:
    poll(0.05)