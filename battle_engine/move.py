from enum import Enum

from stat import *

class MoveCategory(Enum):


    status = 0
    physical = 1
    special = 2

    def get_attack_stat(self):

        if self == MoveCategory.physical:
            return Stat.attack
        elif self == MoveCategory.special:
            return Stat.special_attack
        else:
            return None

    def get_defense_stat(self):

        if self == MoveCategory.physical:
            return Stat.defense
        elif self == MoveCategory.special:
            return Stat.defense
        else:
            return None


class MoveTargets(Enum):


    single = 0
    target_self = 1
    ally = 2
    nearby = 3
    nearby_enemies = 4
    nearby_allies = 5
    ally_side = 6
    enemy_side = 7
    all_mons = 8

    def hits_all_valid(self):

        return not (self == MoveTargets.single or self == MoveTargets.target_self or
                self == MoveTargets.ally)

    def get_valid_targets(self, user_slot, ally_slots, enemy_slots, far_slots = None):

        valid_targets = []
        if (self == MoveTargets.single or self == MoveTargets.ally or
           self == MoveTargets.ally_side or self == MoveTargets.all_mons):
               
            for slot in ally_slots:
                if slot != user_slot:
                    valid_targets.append(slot)
                    
                    
        elif self == MoveTargets.nearby or self == MoveTargets.nearby_allies:
            
            for slot in ally_slots:
                add_to_list = slot != user_slot
                
                if far_slots != None:
                    far_slot_index = 0
                    while far_slot_index < len(far_slots) and add_to_list:
                        add_to_list = slot != far_slots[far_slot_index]
                        far_slot_index += 1
                   
                if add_to_list:
                    valid_targets.append(slot)
                    

        if (self == MoveTargets.target_self or self == MoveTargets.ally or
           self == MoveTargets.ally_side):
               
            valid_targets.append(user_slot)


        if (self == MoveTargets.single or self == MoveTargets.enemy_side or
           self == MoveTargets.all_mons):
               
            for slot in enemy_slots:
                valid_targets.append(slot)


        elif self == MoveTargets.nearby or self == MoveTargets.nearby_enemies:
            
            for slot in enemy_slots:
                add_to_list = True
                
                if far_slots != None:
                    far_slot_index = 0
                    while(far_slot_index < len(far_slots) and add_to_list):
                        add_to_list = slot != far_slots[far_slot_index]
                        far_slot_index += 1
                   
                if(add_to_list):
                    valid_targets.append(slot)
                    

        return valid_targets

    def get_targets(self, selected_target, user_slot, ally_slots, enemy_slots, far_slots = None):

        valid_targets = self.get_valid_targets(user_slot, ally_slots, enemy_slots, far_slots = far_slots)
        if self.hits_all_valid:
            return valid_targets
        else:
            for target in valid_targets:
                if selected_target == target:
                    return [target,]

        #"Move failure" if it's not targeting anything valid
        return None
        
                
    

class MoveDefinition(object):


    def __init__(self, name, pp, move_type, move_category, animation, move_effect = None,
                 bp = None, accuracy = None, targets = MoveTargets.single, priority = 0,
                 crit_modifier = 0, contact = False, sound = False, punch = False,
                 snatchable = False, defrosts = False, reflected = False,
                 blockable = True, copyable = True):

        self.name = name
        self.pp = pp
        self.move_type = move_type
        self.move_category = move_category
        self.animation = animation

        if move_effect == None:
            self.move_effect = MoveEffect()
        else:
            self.move_effect = move_effect
        
        self.bp = bp
        self.accuracy = accuracy
        self.targets = targets

        self.priority = priority
        self.crit_modifier = crit_modifier
        self.contact = contact
        self.sound = sound
        self.punch = punch
        self.snatchable = snatchable
        self.defrosts = defrosts
        self.reflected = reflected
        self.blockable = blockable
        self.copyable = copyable

    
class PokemonMove(object):


    def __init__(self, move_definition):

        self.move_definition = move_definition
        self.pp = moveDefintion.pp
        self.effect = move_definition.effect
        if self.effect:
            self.effect = self.effect.clone()


#Parameters subject to change, so I made them their own object
class MoveEffectParams(object):


    def __init__(self, user, turn_count, targets, target = None, field_state = None):

        self.user = user
        self.targets = targets
        self.target = target
        self.turn_count = turn_count
        self.field_state = field_state


class MoveEffect(object):

    def __init__(self):
        return

    #Will need to override
    def clone(self):
        return MoveEffect()

    def get_pre_execution_flags(self):
        return None

    def move_connected(self, move_effect_params):
        return

    def move_missed(self, move_effect_params):
        return

    def hits_target(self, move_effect_params):
        return True

    def get_custom_accuracy(self, move_effect_params, default_accuracy):
        return default_accuracy
    
    def get_custom_power(self, default_power):
        return default_power

    #To clarify, this method gets passed in the numerical attack stat
    #This is so we can implement Foul Play correctly
    def get_custom_attack(self, default_attack):
        return default_attack

    #This method gets passed in a stat enum, eg. Stat.defense or Stat.special_defense
    #Wonder room is taken into account AFTER this step, if for some reason it matters
    def get_custom_def_stat(self, default_stat):
        return default_stat

    def get_custom_damage(self, move_effect_params, default_damage):
        return default_damage

    #This will get called for every type the target is
    def get_custom_effectiveness(self, move_effect_params, mon_type, default_effectiveness):
        return default_effectiveness

    #Return true if the move fails for some reason
    def check_fail_conditions(self, move_effect_params):
        return False

    def get_hit_probabilities(self):
        return ((1, 100),)

    def get_number_of_turns(self, move_effect_params):
        return 1

    def combatant_acted(self, move, combatant):
        return

    def user_took_damage(self, damaging_move, amount, move_user):
        return

    def ignore_technical_status(self, status):
        return False
