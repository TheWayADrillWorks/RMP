from enum import Enum
import threading
import random

from battle_mode import *
from battle_messaging import *
from mon_type import *
from pokemon import *
from move import *
                               

class Battle(threading.Thread):


    def __init__(self, battle_mode, inverse = False):

        self.message_buffer = MessageBuffer(battle_mode.num_teams())
        self.instruction_queue = InstructionQueue(battle_mode)
        
        self._battle_mode = battle_mode
        self._team_registry_index = 0
        self._turn_count = 0

        num_teams = battle_mode.num_teams()
        self._teams = [None for x in range(num_teams)]
        self._team_is_wild = [False for x in range(num_teams)]
        self._has_remaining_flags = list(self._team_is_wild)

        self._slots = [None for x in range(battle_mode.num_slots())]
        
    def register_team(self, team, wild = False, side = -1):

        team_index = self._battle_mode.find_team_on_side(side)
        if team_index == -1:
            team_index = self._team_registry_index
            self._team_registry_index += 1
        
        self._teams[team_index] = team
        self._team_is_wild[team_index] = wild
        self._has_remaining_flags[team_index] = self._has_remaining(team)

        return slot

    def start_battle(self):

        team_send_out_indicies = [0 for x in range(battle_mode.num_teams())]
            
        for slot in range(len(self._slots)):

            team_index = self._battle_mode.slot_team(slot)
            
            if team_index < len(self._teams):
                team = self._teams[team_index]
               
                if team != None and team_send_out_indicies[team_index] < len(team):
               
                    team_send_out_indicies[team_index] += 1
                    sent_out_mon = team[team_send_out_indicies[team_index]]
                    self._slots[slot] = sent_out_mon

                    status_message = StatusMessage(slot = slot,
                                                   wild = self._team_is_wild[team_index],
                                                   switched_to = BattleMon(sent_out_mon))
               
                    self.message_buffer.push(status_message)

        self.start()

    def _is_side_empty(self):

        for side_index in range(self._battle_mode.num_sides()):
               
            has_remaining = False
            team_index = 0
            while team_index < self._teams and !has_remaining:
                if self._battle_mode.team_side(team_index) == side_index:
                   has_remaining = has_remaining_flags[team_index]

            if !has_remaining:
               return True

        return False

    def _has_remaining(self, team)

        if team != None:
            for active_mon in team:
                if active_mon != None and active_mon.current_hp > 0:
                   return True
               
        return False
    

    def run(self):

        while !self.is_side_empty():

            self._request_general_instructions()
            self._wait_for_general_instructions()

            instruction_queue = self.instruction_queue.get_ordered_instructions
            
            #TODO: Get pre-execution flags

            instruction_valid = [True for x in range(len(instruction_queue))]
            while len(instruction_queue) > 0:
               instruction = instruction_queue.pop(0)
               valid = instruction_valid.pop(0)

               if valid:
                   self._do_instruction(instruction)

            #TODO: Cleanup step, i.e. statuses, weather

            self._turn_count += 1
            #LET'S DO THE TIIMMEE WARP AGGAAAIINNN

    def _request_general_instructions(self):

        self.instruction_queue.clear_instructions()
        for slot in range(len(self._battle_instructions)):
            if self._slots[slot] != None and !self._battle_mode.slot_benched(slot):
                #TODO:Add in restrictions
                self.message_buffer.push(RequestMessage(slot))         


    def _do_instruction(self, instruction)

        if instruction.instruction_type == InstructionType.move:
               
            move = instruction.move
            user = self._slots(instruction.user_slot)

            if user == None:
                return

            ally_slots = self._battle_mode.ally_slots(instruction.user_slot)
            enemy_slots = self._battle_mode.enemy_slots(instruction.user_slot)
            far_slots = self._battle_mode,far_slots(instruction.user_slot)
            
            targets = move.get_targets(instruction.target_slot, instruction.user_slot,
                                       ally_slots, enemy_slots)

            if targets == None:
                self._used_move(user, move.move_definition)
                self.move_failed(user, move.move_definition)
                return
            elif move.pp == 0:
                #TODO: Implement Struggle
                message = Message("%s tried to use %s but it's out of PP!"
                                  %(user.get_name(), move.name))
                self.message_buffer.push(message)
                return
            
            #TODO: Hook for Pressure
            move.pp -= 1
            
            target_mons = [self._slots[slot] for slot in targets]
            self._do_move(move.move_definition, move.effect, user, target_mons)

    def _used_move(self, user, move):
        self.message_buffer.push(Message("%s used %s!" %(user.get_name(),
                                                         move.name)))

    def move_failed(self, user, move):
        self.message_buffer.push(Message("But it failed!"))

    def _do_move(self, move, effect, user, target_mons):

        effect_params = MoveEffectParams(user, self._turn_count, target_mons)
        self._used_move()
        hit = [True for x in target_mons]

        #Roll for hit
        accuracy = move.accuracy)
        if accuracy != None:

            for(index in range(len(target_mons))):
                effect_params.target = target_mons[index]
                final_accuracy = (effect.get_custom_accuracy(effect_params, accuracy) *
                                     target_mons[index].get_evasion_modifier() *
                                     user.get_accuracy_modifier())

                hit[index] = final_accuracy > random.random * 100

        for(target_mon_index in range(len(target_mons))):
            effect_params.target = target_mons[index]
            if(hit[target_mon_index])
                #Do damage calcs
            else
                #Missed
                
                
