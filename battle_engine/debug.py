from mon_type import Type
from move import *
from pokemon import *

def lanturn_test():

    lanturn_species = Species("Lanturn", 177, Type.water, Type.electric,
                              (125, 58, 58, 76, 76, 67))

    surf = MoveDefinition("Surf", 15, Type.water, bp = 90, accuracy = 100,
                               MoveCategory.special, targets = MoveTargets.nearby)

    thunderbolt = MoveDefinition("Thunderbolt", 15, Type.electric, bp = 90, accuracy = 100,
                                      move.MoveCategory.special)

    lanturn_pcmon = PCMon(lanturn_species, 50, Nature.modest,
                          (31, 31, 31, 31, 31, 31),
                          [surf, thunderbolt, None, None],
                          evs=[255, 0, 4, 255, 0, 0])
    
    lanturn_activemon = ActiveMon(lanturn_pcmon)

    tropius_species = Species("Tropius", 357, mon_type.Type.grass, Type.flying,
                              (99, 68, 83, 72, 87, 51))
    
    gust = move.MoveDefinition("Gust", 35, Type.flying, bp = 35, accuracy = 100,
                               MoveCategory.special)

    razor_leaf = move.MoveDefinition("Razor Leaf", 25,  Type.grass, bp = 55, accuracy = 95
                                    MoveCategory.physical,
                                    targets = MoveTargets.nearby_enemies, crit_stage = 2)

    tropius_pcmon = PCMon(tropius_species, 50, Nature.modest,
                          (31, 31, 31, 31, 31, 31),
                          [razor_leaf, gust, None, None])

    tropius_activemon = ActiveMon(tropius_pcmon)

    print("Tropius: ")
    print(tropius_activemon.base_stats)
    print("Lanturn: ")
    print(lanturn_activemon.base_stats)
