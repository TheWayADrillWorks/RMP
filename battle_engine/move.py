from enum import Enum


class Type(Enum):


    bug = 0
    dark = 1
    dragon = 2
    electric = 3
    fairy = 4
    fighting = 5
    fire = 6
    flying = 7
    ghost = 8
    grass = 9
    ground = 10
    ice = 11
    normal = 12
    poison = 13
    psychic = 14
    rock = 15
    steel = 16
    water = 17


class MoveCategory(Enum):


    status = 0
    physical = 1
    special = 2


class MoveTargets(Enum):


    single = 0
    self = 1
    ally = 2
    nearby = 3
    nearby_enemies = 4
    nearby_allies = 5
    ally_side = 6
    enemy_side = 7
    all_mons = 8
    

class MoveDefinition(object):


    def __init__(self, name, pp, bp, accuracy, move_type, move_category,
                 targets = MoveTargets.single, priority = 0, hits = 1,
                 crit_stage = 1, contact = False, sound = False, punch = False,
                 snatchable = False, defrosts = False, reflected = False,
                 blockable = True, copyable = True):

        self.name = name
        self.pp = pp
        self.bp = bp
        self.accuracy = accuracy
        self.move_type = move_type
        self.targets = targets

        self.priority = 0
        self.hits = 1
        self.contact = contact
        self.sound = sound
        self.punch = punch
        self.snatchable = snatchable
        self.defrosts = defrosts
        self.reflected = reflected
        self.blockable = blockable
        self.copyable = copyable


class PokemonMove(object):


    def __init__(self, moveDefinition):

        self.moveDefinition = moveDefinition
        self.pp = moveDefintion.pp

