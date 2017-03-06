from enum import Enum


#We use three terms here:
#
#Side: Cooperating side in a battle. In every mode but the unimplemented
# Battle Royal, there are two sides
#
#Team: The Pokemon in a trainer's party, or a wild Pokemon
#
#Slot: An available space for a Pokemon to be in, to participate in
# a battle. Rotation battles are odd in this regard, as the highest and
# lowest slots on both sides are "benched"
#
#By convention, teams and slots are assigned indicies based on the modulus of
# available slots, so that in every mode except the unimplemented Battle Royal,
# one side will be all even, and the other will be odd.
class BattleMode(Enum):

    singles = 0
    doubles = 1
    multi = 2
    triples = 3
    rotation = 4
    #Not implementing Battle Royal atm for UI reasons

    def num_teams(self):

        if self == BattleMode.multi:
            return 4
        else:
            return 2

    def num_slots_per_team(self):

        if self == BattleMode.singles or self == BattleMode.multi:
            return 1
        elif self == BattleMode.doubles:
            return 2
        else:
            return 3

    def num_slots(self):
                
        return self.num_teams * self.num_slots_per_team

    def num_sides(self):
                
        return 2

    def num_teams(self):
                
        if self == BattleMode.multi:
            return 4
        else:
            return 2

    def find_team_on_side(self, side, registry_index):
                
        if side >= 0 and side < self.num_sides():
            for index in range(registry_index, self.num_sides()):
                if self.team_side[index] == side:
                    return index
        return -1

    def slot_side(self, slot):

        return slot % self.num_sides()
            
    def slot_team(self, slot):

        return slot % self.num_teams()

    def team_side(self, team):

        return team % self.num_sides()

    def slot_benched(self, slot):

        if self == BattleMode.rotation:
            return slot // 2 != 1
        else:
            return False

    def ally_slots(self, user_slot):

        side = self.slot_side(user_slot)
        ally_slots = []
                               
        for slot in range(self.total_slots()):
            if self.slot_side(slot) == side:
                ally_slots.add(slot)

        return ally_slots
                               
    def enemy_slots(self, user_slot):

        side = self.slot_side(user_slot)
        enemy_slots = []
                               
        for slot in range(self.total_slots()):
            if self.slot_side(slot) != side:
                enemy_slots.add(slot)

        return enemy_slots
                               
    def far_slots(self, user_slot):

        if self == BattleMode.triples:
            if user_slot < 2:
                return (4, 5)
            elif user_slot > 3:
                return (0, 1)

        return None
