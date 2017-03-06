from enum import Enum

import math

from move import MoveDefinition, PokemonMove
from stat import *

class Nature(Enum):


    hardy = 1
    lonely = 2
    brave = 3
    adamant = 4
    naughty = 5
    bold = 6
    docile = 7
    relaxed = 8
    impish = 9
    lax = 10
    timid = 11
    hasty = 12
    serious = 13
    jolly = 14
    naive = 15
    modest = 16
    mild = 17
    quiet = 18
    bashful = 19
    rash = 20
    calm = 21
    gentle = 22
    sassy = 23
    careful = 24
    quirky= 25

    def get_increased_stat(self):

        if (self == Nature.lonely or self == Nature.brave or
           self == Nature.adamant or self == Nature.naughty):
            return Stat.attack
        
        elif (self == Nature.bold or self == Nature.relaxed or
             self == Nature.impish or self == Nature.lax):
            return Stat.defense
        
        elif (self == Nature.timid or self == Nature.hasty or
             self == Nature.jolly or self == Nature.naive):
            return Stat.speed
        
        elif (self == Nature.modest or self == Nature.mild or
             self == Nature.quiet or self == Nature.rash):
            return Stat.special_attack

        elif (self == Nature.calm or self == Nature.gentle or
             self == Nature.sassy or self == Nature.careful):
            return Stat.special_defense

        #neutral natures
        else:
            return None

    def get_decreased_stat(self):

        if (self == Nature.bold or self == Nature.timid or
           self == Nature.modest or self == Nature.calm):
            return Stat.attack
        
        elif (self == Nature.lonely or self == Nature.hasty or
             self == Nature.mild or self == Nature.gentle):
            return Stat.defense
        
        elif (self == Nature.brave or self == Nature.relaxed or
             self == Nature.quiet or self == Nature.sassy):
            return Stat.speed
        
        elif (self == Nature.adamant or self == Nature.impish
             or self == Nature.jolly or self == Nature.careful):
            return Stat.special_attack

        elif (self == Nature.naughty or self == Nature.lax
             or self == Nature.naive or self == Nature.rash):
            return Stat.special_defense

        #neutral natures
        else:
            return None




class Species(object):


    def __init__(self, name, dex_number, type_one, type_two, base_stats):
    
        self.name = name
        self.dex_number = dex_number
        self.type_one = type_one
        self.type_two = type_two

        self.base_stats = base_stats


class PCMon(object):


    def __init__(self, species, level, nature, ivs, moves,
                 evs=[0, 0, 0, 0, 0, 0], nickname = None):

        self.species = species
        self.level = level
        self.nature = nature
        self.ivs = ivs
        self.evs = evs
        self.moves = moves
        self.nickname = nickname

    def get_name(self):

        if(self.nickname == None):
            return self.species.name
        else:
            return nickname

class ActiveMon(object):


    def __init__(self, base_mon):

        self._base_mon = base_mon

        self._moves = [PokemonMove(move) for move in base_mon.moves]

        self.major_status = None
        self.minor_status = []
        self.technical_status = []
        self,reset_stat_modifiers()
        
        self.update_base_stats()
        self.current_hp = self.base_stats[Stat.HP.value]
        
    def update_base_stats(self):

        #Hairy math ahead
        base_HP = math.floor((2*self._base_mon.species.base_stats[Stat.HP.value] +
                              (self._base_mon.evs[Stat.HP.value]/4) +
                              self._base_mon.ivs[Stat.HP.value]) *
                              self._base_mon.level/100)
        base_HP += 10 + self._base_mon.level

        stat_list = [base_HP];

        for stat_index in range(1, 6):
            stat = math.floor((2*self._base_mon.species.base_stats[stat_index] +
                              (self._base_mon.evs[stat_index]/4) +
                              self._base_mon.ivs[stat_index]) *
                              self._base_mon.level/100)
            stat += 5

            increased_stat = self._base_mon.nature.get_increased_stat()
            decreased_stat = self._base_mon.nature.get_decreased_stat().value
            
            if increased_stat != None and stat_index == increased_stat.value:
                stat = math.floor(stat * 1.1)
            elif decreased_stat != None and stat_index == decreased_stat.value:
                stat = math.floor(stat*0.9)

            stat_list.append(stat)
            
        self._base_stats = tuple(stat_list)

    def reset_stat_modifiers(self):
        
        #Crit Modifier, Atk, Def, Sp. A, Sp. D, Speed, Accuracy, Evasion
        self.stat_modifiers = [1, 0, 0, 0, 0, 0, 0, 0]

    def get_unmodified_stat(self, stat):

        return self._base_stats[stat.value]

    def get_modified_stat(self, stat):

        stat = self.get_unmodified_stat(stat)
        stat_modifier = self.stat_modifiers[stat.value]

        if stat_modifier > 0:
            stat *= 1 + (0,5 * stat_modifier)
        elif stat_modifier < 0:
            stat /= 1 + (-0.5 * stat_modifier)

        stat = math.floor(stat)
        return stat
        

    def get_accuracy_modifier(self):

        stage = self.stat_modifiers[6]
        if stage > 0:
            return 1 + (stage / 3)
        elif stage < 0:
            return 1 / (1 + (stage / -3))
        else:
            return 1

    def get_evasion_modifier(self):

        stage = self.stat_modifiers[7]
        if stage > 0:
            return 1 / (1 + (stage / 3))
        elif stage < 0:
            return 1 + (stage / -3)
        else:
            return 1

    #gives crit rate out of 10,000
    def get_crit_rate(self, modifier):

        #TODO: Super luck hook in here?
        stage = self.stat_modifiers[0] + modifier
        if stage == 1:
            return 625
        elif stage == 2:
            return 1250
        elif stage == 3:
            return 5000
        else:
            return 10000
        
    def get_move(self, move_index):

        if move_index < len(self._moves):
            return self._moves[move_index]
        else:
           return None

    def get_name(self):

        return self.base_mon.get_name()

    def get_level(self):

        return self.base_mon.level


#Minimally represents an opponent mon for the UI
class BattleMon(object):

    def __init__(self, active_mon):

        self.name = active_mon.base_mon.get_name()
        self.hp_percent = active_mon.current_hp / active_mon.base_stats[Stat.HP.value]
        self.status = active_mon.status
        self.level = active_mon.level
        

