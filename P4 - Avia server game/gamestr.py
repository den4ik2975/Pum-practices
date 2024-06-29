from random import choice


class Player:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.plant_num = 2
        self.material_num = 4
        self.fighter_num = 2
        self.cash = 10000
        self.fighter_ordered = 0
        self.plants_building = []
        self.is_finished = False
        self.is_bunkrupt = False

    def calculate_capitalization(self, material_price, fighter_price):
        cap = 0
        cap += self.plant_num * 5000
        cap += self.material_num * material_price
        cap += self.fighter_num * fighter_price
        cap += self.cash
        return cap


class Game:
    def __init__(self, players, market_level, market_levels, market_chances, month_num):
        self.players_profiles = dict()
        self.players_raw_orders = dict()
        self.players_fighter_orders = dict()
        self.players_num = players
        self.market_level = market_level
        self.market_levels = market_levels
        self.market_chances = market_chances
        self.month_num = month_num
        self.cur_month = 0
        self.is_started = False
        self.is_ended = False
        self.players_finished = 0

    def calculate_values(self):
        self.material_bank = int(self.market_levels[str(self.market_level)][0] * self.players_num)
        self.min_material_price = self.market_levels[str(self.market_level)][1]
        self.fighter_bank = int(self.market_levels[str(self.market_level)][2] * self.players_num)
        self.max_fighter_price = self.market_levels[str(self.market_level)][3]

    @staticmethod
    def can_pay(cur_player, order):
        return True if cur_player.cash - (order[1][0] * order[1][1]) >= 0 else False

    def bunkrupt_check(self, player):
        if player.cash < 0:
            player.is_bunkrupt = True
            self.players_num -= 1
            if self.players_num is 0:
                self.is_ended = True

    def raw_handling(self):
        self.sorted_players_raw_orders = sorted(self.players_raw_orders.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True)

        for order in self.sorted_players_raw_orders:
            cur_player = self.players_profiles[order[0]]
            if self.material_bank == 0:
                break
            if order[1][0] <= self.material_bank:
                if self.can_pay(cur_player, order):
                    self.material_bank -= order[1][0]
                    self.players_profiles[order[0]].cash -= order[1][0] * order[1][1]
                    self.players_profiles[order[0]].material_num += order[1][0]
                else:
                    self.bunkrupt_check(cur_player)

            elif order[1][0] > self.material_bank:
                if self.can_pay(cur_player, order):
                    self.players_profiles[order[0]].cash -= self.material_bank * order[1][1]
                    self.players_profiles[order[0]].material_num += self.material_bank
                    break
                else:
                    self.bunkrupt_check(cur_player)

        self.players_raw_orders.clear()

    def plane_handling(self):
        self.sorted_players_fighter_orders = sorted(self.players_fighter_orders.items(), key=lambda item: (-1 * item[1][1], item[1][0]), reverse=True)

        for order in self.sorted_players_fighter_orders:
            cur_player = self.players_profiles[order[0]]
            if self.fighter_bank == 0:
                break
            if order[1][0] <= self.fighter_bank:
                self.fighter_bank -= order[1][0]
                cur_player.cash += order[1][0] * order[1][1]
                cur_player.fighter_num -= order[1][0]

            elif order[1][0] > self.fighter_bank:
                cur_player.cash += self.fighter_bank * order[1][1]
                cur_player.fighter_num -= self.fighter_bank
                break

        self.players_fighter_orders.clear()

    def fighter_produce(self):
        for player in self.players_profiles.values():
            player.fighter_num += player.fighter_ordered
            player.fighter_ordered = 0

    def plant_checker(self):
        for player in self.players_profiles.values():
            player.plants_building = [month + 1 for month in player.plants_building]
            analys = player.plants_building[:]
            for month in analys:
                if month == 4:
                    player.plant_num += 1
                    player.cash -= 2500
                    del player.plants_building[player.plants_building.index(4)]

            self.bunkrupt_check(player)


    def calculate_taxes(self):
        for player in self.players_profiles.values():
            player.cash -= player.material_num * 300
            player.cash -= player.fighter_num * 500
            player.cash -= player.plant_num * 1000

            self.bunkrupt_check(player)

    def market_level_choice(self):
        self.market_level = choice(self.market_chances[self.market_level])
