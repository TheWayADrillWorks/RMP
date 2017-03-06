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

                    self.message_switch_in(slot, wild = self._team_is_wild[team_index])

        self.start()

    def _is_side_empty(self):

        for side_index in range(self._battle_mode.num_sides()):
               
            has_remaining = False
            team_index = 0
            while team_index < self._teams and not has_remaining:
                if self._battle_mode.team_side(team_index) == side_index:
                   has_remaining = has_remaining_flags[team_index]

            if not has_remaining:
               return True

        return False

    def _has_remaining(self, team):

        if team != None:
            for active_mon in team:
                if active_mon != None and active_mon.current_hp > 0:
                   return True
               
        return False
    

    def run(self):

        while not self.is_side_empty():

            self._request_general_instructions()
            self.instruction_queue.wait_for_general_instructions()

            instruction_queue = self.instruction_queue.get_ordered_instructions()
            
            #TODO: Get pre-execution flags

            self._instruction_valid = [True for x in range(len(instruction_queue))]
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
            if self._slots[slot] != None and not self._battle_mode.slot_benched(slot):
                #TODO:Add in restrictions
                self.message_buffer.push(RequestMessage(slot))         

    def _do_instruction(self, instruction):

        if instruction.instruction_type == InstructionType.move:
               
            move = instruction.move
            user_slot = instruction.user_slot
            user = self._slots[user_slot]

            if self._slots[user_slot] == None:
                return

            ally_slots = self._battle_mode.ally_slots(instruction.user_slot)
            enemy_slots = self._battle_mode.enemy_slots(instruction.user_slot)
            far_slots = self._battle_mode,far_slots(instruction.user_slot)
            
            target_slots = move.get_targets(instruction.target_slot, instruction.user_slot,
                                       ally_slots, enemy_slots)
            
            if move.pp == 0:
                #TODO: Implement Struggle
                self.message_out_of_pp(user_slot, move.move_definition)
                return
            
            #TODO: Hook for Pressure
            move.pp -= 1

            if targets == None:
                #TODO: Change targets for single targeting move
                self.message_used_move(user_slot, move.move_definition)
                self.message_move_failed(user_slot, move.move_definition)
                return
            
            target_mons = [self._slots[slot] for slot in targets]
            self._do_move(move.move_definition, move.effect, user_slot, target_mons)
            

    def _do_move(self, move, effect, user_slot, target_mon_slots):

        user = self._slots[user]
        target_mons = [self._slots[slot] for slot in target_mon_slots]
        
        effect_params = MoveEffectParams(user, self._turn_count, target_mons)

        if effect.check_fail_conditions(effect_params):
            self.message_used_move(user_slot, move.move_definition)
            self.message_move_failed(user_slot, move.move_definition)
            return

        hit = [True for x in target_mons]

        #Roll for hit
        accuracy = move.accuracy
        if accuracy != None:

            for index in range(len(target_mons)):
                effect_params.target = target_mons[index]
                final_accuracy = (effect.get_custom_accuracy(effect_params, accuracy) *
                                     target_mons[index].get_evasion_modifier() *
                                     user.get_accuracy_modifier())

                hit[index] = final_accuracy > random.randint(0, 99)

        for target_mon_index in range(len(target_mons)):

            target = target_mons[target_mon_index]
            target_slot = target_mon_slots[target_mon_index]
            effect_params.target = target

            if hit[target_mon_index]:
                #Hit
                if target_mon_index == 0 :
                    self.message_used_move(user, move, animate = True,
                                           target_slot = target_slot)
                
                self._handle_move_hit(move, effect, user, target, target_slot, effect_params)                        
                
            else:
                #Missed
                if target_mon_index == 0:
                    self.message_used_move(user, move, animate = len(target_mons) > 1,
                                           target_slot = target_slot)
                if len(target_mons > 1):
                    self.message_avoided(target)
                else:
                    self.message_missed(user)

    def _handle_move_hit(self, move, effect, user, target, target_slot,
                         effect_params, hits_multiple, last_hit = True):

        power = effect.get_custom_power(move.bp)

        if not effect.hits_target(effect_params):
            return
        
        if power != None:
            default_attack_stat = move.move_category.get_attack_stat()
                    
            if default_attack_stat != None:
                #TODO: Hook for Unaware
                attack = user.get_modified_stat(default_attack_stat)
                attack = effect.get_custom_attack(attack)

                defense_stat = move.move_category.get_defense_stat()
                defense_stat = effect.get_custom_def_stat(default_defense_stat)
                #TODO: Hook for Wonder Room

                defense = 0
                crit = user.get_crit_rate(move.crit_modifier) > random.randint(0, 9999)
                #TODO: Hook for Lucky Chant, Battle Armor
                if crit:
                    defense = target.get_unmodified_stat(defense_stat)
                else:
                    defense = target.get_modified_stat(defense_stat)

                effectiveness = self._get_effectiveness(move, effect, target)

                damage = ((2 * user.get_level() / 5) + 2) * attack * power / defense
                damage = ((damage / 50) + 2) * random.randint(0, 100)
                if crit:
                    #TODO:Hook for Sniper
                    damage *= 1.5
                
                pre_type_damage = damage
                damage *= self.get_stab(user, move) * effectiveness

                #TODO: Apply other bonuses (e.g. weather, levitate)

                new_damage = effect.get_custom_damage(effect_params, damage)

                #Actually... maybe move this into ActiveMon?
                target.current_hp -= new_damage
                if target.current_hp < 0:
                    #TODO: Hook for Focus Sash/Band/Sturdy
                    #and user_took_damage
                    target.current_hp = 0
                
                if crit and new_damage == damage:
                    self.message_crit()

                if new_damage > 0:
                    self.message_hp_change(target)

                if pre_type_damage > 0 and new_damage == damage::
                    if hits_mulitple:
                        self.message_effectiveness(effectiveness, target_slot)
                    else:
                        self.message_effectiveness(effectiveness)

                if target.current_hp == 0:
                    self._faint(target_slot)

        if target.current_hp > 0:
            effect.move_connected(effect_params)

    def _get_effectiveness(move, effect, target):
        
        move_type = move.move_type
        effectiveness = 1

        target_types = target.get_types()

        for mon_type in target_types:
            partial_eff = mon_type.get_effectiveness(move_type)
            effectiveness *= effect.get_custom_effectiveness(partial_eff)

        return effectiveness

    def _faint(self, target_slot):
        #TODO
        return
        

    #---Message Convinience Methods---
    def message_crit(self):
        self.message(text = "Critical hit!")
        
    def message_hp_change(self, target_slot):
        StatusMessage message = StatusMessage(slot = target_slot,
                                              hp_value = target.current_hp,
                                              hp_percent = target.get_hp_percent)
        return

    def message_battle_over(self, target_slot):
        StatusMessage message = StatusMessage(battle_over = True)
        return

    def message_effectiveness(self, effectiveness, target = None):
        if effectiveness > 1:
            self.message(text = "It's super effective!")
        elif effectiveness == 0:
            if target == None:
                self.message(text = "It had no effect!")
            else:
                self.message(text = ("It had no effect on ", user.get_name(), "!"),
                             localize_flags = (True, False))
        elif effectiveness < 1: 
            self.message(text = "It's not very effective...")
        
    def message_out_of_pp(self, user_slot, move = None):
        user = self._slots[user]
        if move == None:
            self.message(text = (user.get_name(), " is out of PP!"),
                         localize_flags = (False,))
        else:
            self.message(text = (user.get_name(), " tried to use ", move.name,
                                 " but is out of PP!"), localize_flags = (False,))
        
    def message_avoided(self, target):
        self.message(text = (target.get_name(), " dodged the attack!"),
                     localize_flags = (False,))

    def message_missed(self, user):
        self.message(text = (user.get_name(), "'s attack missed!"),
                     localize_flags = (False,))
    
    def message_switch_in(self, slot, wild = False):
        status_message = StatusMessage(slot = slot, wild = wild,
                                       switched_to = BattleMon(self._slots[slot]))
        self.message_buffer.push(status_message)
            
    def message_used_move(self, user_slot, move, target_slot = None, animate = False):
        user = self._slots[user]
        if(animate):
            self.message(text = (user.get_name(), " used ", move.name, "!"),
                         localize_flags = (False,), user_slot = user_slot,
                         target_slot = target_slot, animation = move.animation)
        else:
            self.message(text = (user.get_name(), " used ", move.name, "!"),
                         localize_flags = (False,), user_slot = user_slot,
                         target_slot = target_slot)

    def message_move_failed(self):
        self.message(text = "But it failed!")

    def message(self, text = None, localize_flags = None, animation = None,
                user_slot = None, target_slot = None):
                              
        message_text = None
        if text != None:
            message_text = LocalizableText(text, localize_flags)

        self.message_buffer.push(Message(text = message_text, animation = animation,
                                         user = user_slot, target = target_slot))
