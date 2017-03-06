from enum import Enum

import time
import random

from battle_mode import BattleMode


#---Messages from the engine to the scene---


class LocalizableText(object):

    #Note that localize_flags is not only optional but need only
    #indicate localization up to the last non-localized string in text
    def __init(self, text, localize_flags = None):
        self._text = text
        self._localize_flags = localize_flags

    #TODO:pass in translation module
    def get_text(self):
        if isinstance(self._text, str):
            if self._localize_flags != None and not self._localize_flags:
                return self._text
            else:
                #TODO:Translate dis
                return self._text
        else:
            final_string = ""
            for index in range(len(text)):
                if (self._localize_flags != None and index < len(self._localize_flags) and
                   not self._localize_flags[index]):
                    final_string += self._text[index]
                else:
                    #TODO:Translate dis
                    final_string += self._text[index]
                    
            return final_string


class Message(object):


    def __init__(self, animation = None, text = None, user = None, target = None):

        self.animation = animation
        self.text = text
        self.user = user
        self.target = target
    

class StatusMessage(object):

    def __init__(self, slot = -1, status = -1, hp_value = -1, hp_percent = -1,
                 switched_to = None, battle_over = False, wild = False):
        
        self.status = status
        self.hp_value = hp_value
        self.hp_fraction = hp_fraction
        self.switched_to = switched_to
        self.battle_over = battle_over


class RequestMessage(object):

    def __init__(self, slot, restrictions = None):

        self.restrictions = restrictions
        self.slot = slot
        
        
class MessageBuffer(object):


    def __init__(self, num_listeners):

        #This lock is set up to be >0 when the buffer is being read
        #and -1 when it is being written to
        self._lock = 0

        self._buffer = []

        self._listener_positions = [0 for x in range(num_listeners)]


    def peek(self, listener_num):

        self._obtain_read_lock()
        messages = []
        listener_position = self._listener_positions[listener_num]
        if listener_position < len(self._buffer):
            messages = self._buffer[listener_position:]
                
        self._release_read_lock()
        return messages

    
    def pop(self, listener_num, num_messages):

        self._obtain_write_lock()

        if self._listener_positions[listener_num] + num_messages < len(self._buffer) + 1:
            self._listener_positions[listener_num] += num_messages
            
        self._release_write_lock()
        self._clear_old()
        
    def push(self, message):

        self._obtain_write_lock()
        self._buffer.append(message)
        self._release_write_lock()
        
    def _clear_old(self):
    
        self._obtain_write_lock()

        lowest_position = -1
        for listener_position in self._listener_positions:
            if lowest_position == -1 or lowest_position < listener_position:
                lowest_position = listener_position

        if lowest_position > 0:
            for index in range(len(self._listener_positions)):
                self._listener_positions[index] -= lowest_position

        for index in range(lowest_position):
                self._buffer.pop(0)
        
        self._release_write_lock()

    def _obtain_write_lock(self):

        while self.lock != 0:
            time.sleep(0.125)

        self._lock = -1
        
    def _release_write_lock(self):
    
        self._lock = 0

    def _obtain_read_lock(self):

        while self.lock < 0:
            time.sleep(0.125)

        self._lock += 1

    def _release_read_lock(self):

        self._lock -= 1

#---Messages from the scene to the engine---
class InstructionType(Enum):

    move = 0
    item = 1
    switch_mon = 2
                
    #Internal instruction types, would not recommend giving via the scene                
    request_switch = 3
    random_switch = 4

    
class BattleInstruction(object):


    def __init__(self, instruction_type, user_slot, target_slot = -1, speed = 0,
                 priority = 0, move = None, item = None):

        self.instruction_type = instruction_type
        self.user_slot = user_slot
        self.target_slot = target_slot
        self.speed = speed
        self.priority = priority
        self.move = move
        self.item = item


class InstructionQueue(object):


    def __init__(self, battle_mode):

        self._battle_mode = battle_mode
        self._battle_instructions = [None for x in range(battle_mode.num_slots())]

    #call from scene only
    def give_battle_instruction(self, slot, battle_instruction):

        #Should do some validation in here, eventually.
        #Maybe as a multiplayer server thing
        self._battle_instructions[slot] = battle_instruction
    

    #call from engine only
    def clear_instructions(self):

        for slot in range(len(self._battle_instructions)):
            self._battle_instructions[slot] = None

    #Call from engine thread only
    def wait_for_general_instructions(self, slots):
                               
        keep_waiting = True
               
        while keep_waiting:
               
            keep_waiting = False
            slot = 0
            while slot < len(self._battle_instructions) and not keep_waiting:
               if slots[slot] != None and not self._battle_mode.slot_benched(slot):
                    keep_waiting = self._battle_instructions[slot] == None
               slot += 1

            if keep_waiting:
               time.sleep(0.125)
                               
    #Call from engine thread only
    def wait_for_switch(self, slot):
        
        keep_waiting = True
               
        while keep_waiting:

            if self._battle_instructions[slot] == None:
                instruction = self._battle_instructions[slot].instruction
                keep_waiting = instruction_type != InstructionType.switch_mon
                           
            if keep_waiting:
               time.sleep(0.125)

    #call from engine only
    def get_ordered_instructions(self, trick_room = False):

        instruction_queue = list(self._battle_instructions)

        #this ensures speed ties are random
        random.shuffle(instruction_queue)

        #since order is preserved, priority ties will be sorted by speed
        instruction_queue = sorted(instruction_queue, key=lambda instruction:instruction.speed, reversed=trick_room)
        instruction_queue = sorted(instruction_queue, key=lambda instruction:instruction.priority)

        return instruction_queue
