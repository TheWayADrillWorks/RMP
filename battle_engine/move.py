from enum import Enum


class MoveCategory(Enum):


    status = 0
    physical = 1
    special = 2


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

    def hits_all_valid(self)

        return !(self == MoveTargets.single or self == MoveTargets.target_self or
                self == MoveTargets.ally)

    def get_valid_targets(self, user_slot, ally_slots, enemy_slots, far_slots = None):

        valid_targets = []
        if self == MoveTargets.single or self == MoveTargets.ally or
           self == MoveTargets.ally_side or self == MoveTargets.all_mons:
               
            for slot in ally_slots:
                if slot != user_slot):
                    valid_targets.append(slot)
                    
                    
        elif self == MoveTargets.nearby or self == MoveTargets.nearby_allies:
            
            for slot in ally_slots:
                add_to_list = slot != user_slot
                
                if far_slots != None:
                    far_slot_index = 0
                    while(far_slot_index < len(far_slots) and add_to_list):
                        add_to_list = slot != far_slots[far_slot_index]
                        far_slot_index += 1
                   
                if add_to_list:
                    valid_targets.append(slot)
                    

        if self == MoveTargets.target_self or self == MoveTargets.ally or
           self == MoveTargets.ally_side:
               
            valid_targets.append(user_slot)


        if self == MoveTargets.single or self == MoveTargets.enemy_side or
           self == MoveTargets.all_mons:
               
            for slot in enemy_slots:
                valid_targets.append(slot)


        elif(self == MoveTargets.nearby or self == MoveTargets.nearby_enemies):
            
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
        if self.hits_all_valid
            return valid_targets
        else
            for target in valid_targets:
                if selected_target == target:
                    return [target,]

        #"Move failure" if it's not targeting anything valid
        return None
        
                
    

class MoveDefinition(object):


    def __init__(self, name, pp, move_type, move_category, move_effect = None, bp = None,
                 accuracy = None, targets = MoveTargets.single, priority = 0,
                 crit_stage = 1, contact = False, sound = False, punch = False,
                 snatchable = False, defrosts = False, reflected = False,
                 blockable = True, copyable = True):

        self.name = name
        self.pp = pp
        self.bp = bp
        self.accuracy = accuracy
        self.move_type = move_type
        self.targets = targets

        self.move_effect = move_effect

        self.priority = priority
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

    #Will need to override
    def clone(self):
        return MoveEffect()

    def get_pre_execution_flags(self):
        return None

    def move_connected(self, move_effect_params):

    def move_missed(self, move_effect_params):

    def get_custom_accuracy(self, move_effect_params, default_accuracy):
        return default_accuracy
    
    def get_custom_power(self, default_power):
        return default_power
    
    def get_custom_attack_stat(self, default_stat):
        return default_stat

    #Wonder room is taken into account AFTER this step, if for some reason it matters
    def get_custom_def_stat(self, move_effect_params, default_stat):
        return default_stat

    def get_custom_damage(self, move_effect_params, default_damage):
        return default_damage

    #This will get called for every type the target is
    def get_custom_effectiveness(self, move_effect_params, mon_type, default_effectiveness):
        return default_effectiveness

    def check_fail_conditions(self, move_effect_params):
        return False

    def get_number_of_hits(self):
        return 1

    def get_number_of_turns(self, move_effect_params):
        return 1

    def combatant_acted(self, move, combatant):

    def user_took_damage(self, damaging_move, amount, move_user):

    def ignore_technical_status(self, status):
        return False
