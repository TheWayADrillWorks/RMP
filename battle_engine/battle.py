from enum import Enum
import time
import pokemon
import move

class MessageType(Enum):


    choose_action = 0
    choose_switch = 1

    #Will be in a tuple with used_move, move_id, originator #,
    #receiver #(s), and whether to animation
    used_move = 2

    #Will be in a tuple with receiver and (optionally) effectiveness
    #Zero damage/effectiveness indicates immunity
    move_damage = 3
    
    #Will be in a tuple with #receiver #
    move_missed = 4

    #Will be in a tuple with combatant id
    fainted = 5
    battle_finished = 6
    

class MessageBuffer(object):


    def __init__(self, num_listeners):

        self._locked = False

        self._buffer = []

        self._listener_positions = []
        
        for(x in range(num_listeners)):
            self._listener_positions.append(0)


    #This looks complicated, but all I'm doing is grabbing a message from the listener's spot
    #then cleaning up old messages that every listener has gotten.  There is some locking around
    #getting messages but 
    def pop(self, listener_num):

        while(self.locked):
            time.sleep(0.125)

        message = None
        self._locked = True

        listener_position = self._listener_positions[listener_num]
        if(listener_position < len(self.buffer)):

            message = self._buffer[listener_position]
            listener_position += 1
            self._listener_positions[listener_num] += 1
            
            is_lowest = true
            index = 0
            while(index < len(self._listener_positions) && is_lowest):
                if(listener_num != index):
                    is_lowest = self._listener_positions[listener_num]
                                > self._listener_positions[index]
                index += 1

            if(is_lowest):
                for(index in range(self._listener_positions)):
                    self._listener_positions -= 1
                self._buffer.pop(0)
                
        self._locked = False
        return message


class Battle(object):






        
