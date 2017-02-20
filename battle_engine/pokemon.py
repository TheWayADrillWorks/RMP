from enum import Enum
import move
import math


class Stat(Enum):    


    HP = 0
    attack = 1
    defense = 2
    special_attack = 3
    special_defense = 4
    speed = 5
    

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

        if(self == Nature.lonely or self == Nature.brave or
           self == Nature.adamant or self == Nature.naughty):
            return Stat.attack
        
        elif(self == Nature.bold or self == Nature.relaxed or
             self == Nature.impish or self == Nature.lax):
            return Stat.defense
        
        elif(self == Nature.timid or self == Nature.hasty or
             self == Nature.jolly or self == Nature.naive):
            return Stat.speed
        
        elif(self == Nature.modest or self == Nature.mild or
             self == Nature.quiet or self == Nature.rash):
            return Stat.special_attack

        elif(self == Nature.calm or self == Nature.gentle or
             self == Nature.sassy or self == Nature.careful):
            return Stat.special_defense

        #neutral natures
        else:
            return None

    def get_decreased_stat(self):

        if(self == Nature.bold or self == Nature.timid
           or self == Nature.modest or self == Nature.calm):
            return Stat.attack
        
        elif(self == Nature.lonely or self == Nature.hasty
             or self == Nature.mild or self == Nature.gentle):
            return Stat.defense
        
        elif(self == Nature.brave or self == Nature.relaxed
             or self == Nature.quiet or self == Nature.sassy):
            return Stat.speed
        
        elif(self == Nature.adamant or self == Nature.impish
             or self == Nature.jolly or self == Nature.careful):
            return Stat.special_attack

        elif(self == Nature.naughty or self == Nature.lax
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
                 evs=[0, 0, 0, 0, 0, 0]):

        self.species = species
        self.level = level
        self.nature = nature
        self.ivs = ivs
        self.evs = evs
        self.moves = moves


class ActiveMon(object):


    def __init__(self, base_mon):

        self.base_mon = base_mon
        self.update_base_stats()
        
    def update_base_stats(self):

        #Hairy math ahead
        base_HP = math.floor((2*self.base_mon.species.base_stats[Stat.HP.value] +
                              (self.base_mon.evs[Stat.HP.value]/4) +
                              self.base_mon.ivs[Stat.HP.value]) *
                              self.base_mon.level/100)
        base_HP += 10 + self.base_mon.level

        stat_list = [base_HP];

        for stat_index in range(1, 6):
            stat = math.floor((2*self.base_mon.species.base_stats[stat_index] +
                              (self.base_mon.evs[stat_index]/4) +
                              self.base_mon.ivs[stat_index]) *
                              self.base_mon.level/100)
            stat += 5
            
            if(stat_index == self.base_mon.nature.get_increased_stat().value):
                stat = math.floor(stat * 1.1)
            elif(stat_index == self.base_mon.nature.get_decreased_stat().value):
                stat = math.floor(stat*0.9)

            stat_list.append(stat)
            
        self.base_stats = tuple(stat_list)                  






def lanturn_test():

    lanturn_species = Species("Lanturn", 177, move.Type.water, move.Type.electric,
                              (125, 58, 58, 76, 76, 67))

    surf = move.MoveDefinition("Surf", 15, 90, 100, move.Type.water,
                               move.MoveCategory.special, targets = move.MoveTargets.nearby)

    thunderbolt = move.MoveDefinition("Thunderbolt", 15, 90, 100, move.Type.electric,
                                      move.MoveCategory.special)

    lanturn_pcmon = PCMon(lanturn_species, 50, Nature.modest,
                          (31, 31, 31, 31, 31, 31),
                          [surf, thunderbolt, None, None],
                          evs=[255, 0, 4, 255, 0, 0])
    
    lanturn_activemon = ActiveMon(lanturn_pcmon)

    tropius_species = Species("Tropius", 357, move.Type.grass, move.Type.flying,
                              (99, 68, 83, 72, 87, 51))
    
    gust = move.MoveDefinition("Gust", 35, 40, 100, move.Type.flying, move.MoveCategory.special)

    razor_leaf = move.MoveDefinition("Razor Leaf", 15, 90, 100, move.Type.water,
                                    move.MoveCategory.special,
                                    targets = move.MoveTargets.nearby, crit_stage = 2)

    tropius_pcmon = PCMon(tropius_species, 50, Nature.modest,
                          (31, 31, 31, 31, 31, 31),
                          [razor_leaf, gust, None, None])

    tropius_activemon = ActiveMon(tropius_pcmon)

    print("Tropius: ")
    print(tropius_activemon.base_stats)
    print("Lanturn: ")
    print(lanturn_activemon.base_stats)
