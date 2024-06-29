from flask import Flask, jsonify, request
from const import market_levels, market_chances
from gamestr import Game, Player
import sys
import threading


def is_valid_addr(ip):
    if ip.count('.') == 3:
        for i in ip.split('.'):
            if 0 <= int(i) <= 255:
                pass
            else:
                return False
        return True


def set_params():
    if len(sys.argv) == 4:
        if is_valid_addr(sys.argv[1]):
            return [sys.argv[1], sys.argv[2], sys.argv[3], -1]
        else:
            print('wrong ip')
    elif len(sys.argv) == 5:
        if is_valid_addr(sys.argv[1]):
            return [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
        else:
            print('wrong ip')
    else:
        print('Try again')
    return [False]


params = set_params()
if len(params) == 4:
    ip, port, players, month = params[0], params[1], int(params[2]), int(params[3])
else:
    sys.exit()
#ip = '127.0.0.1'
#port = 5000
#players = 2
#month = -1
id_counter = 1

server = Flask(__name__)
game = Game(players=players, market_level='3', market_levels=market_levels, market_chances=market_chances, month_num=month)
game.calculate_values()


@server.post('/connect')
def index():
    data = request.get_json()
    global id_counter
    if game.is_started is False and len(game.players_profiles) < game.players_num:
        player = Player(request.remote_addr, data['name'])
        game.players_profiles[id_counter] = player
        id_counter += 1
        print(game.players_profiles)
        return jsonify(data=f'{data["name"]} you successfully joined the game', id=id_counter - 1, status='ok')
    else:
        return jsonify(data='Game has already started or lobby is full', status='no')


@server.post('/info')
def user_info():
    cur_player = game.players_profiles[request.get_json()['id']]
    if game.is_started is False:
        return jsonify(data='Waiting for other players', status='0')
    if game.is_ended:
        return jsonify(data=f'Game ended, winner is {next(iter(game.players_profiles))[1].name}', status='10')
    if cur_player.is_bunkrupt:
        return jsonify(data='You are a bunkrupt', status = '-1')
    if cur_player.is_finished is False and game.is_started is True:
        market_lvl = game.market_level
        raw_price = game.min_material_price
        plane_price = game.max_fighter_price
        plants = cur_player.plant_num
        cash = cur_player.cash
        fighters = cur_player.fighter_num
        raw = cur_player.material_num
        return jsonify(market_lvl=market_lvl, raw_price=raw_price, plane_price=plane_price, plants=plants, cash=cash,
                       fighters=fighters, raw=raw, status='1')
    if cur_player.is_finished is True:
        return jsonify(data='Waiting other players to finish', status='2')


@server.post('/buy_raw')
def purchase():
    data = request.get_json()
    cur_player = game.players_profiles[data['id']]
    if int(data['price']) >= int(game.min_material_price) and int(data['number']) > 0 and int(data['number']) * int(data['price']) <= cur_player.cash:
        game.players_raw_orders[data['id']] = [int(data['number']), int(data['price'])]
        print(game.players_raw_orders)
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/sell_planes')
def get_order():
    data = request.get_json()
    cur_player = game.players_profiles[data['id']]
    if int(data['price']) <= int(game.max_fighter_price):
        game.players_fighter_orders[data['id']] = [int(data['number']), int(data['price'])]
        print(game.players_fighter_orders)
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/produce')
def plane_order():
    data = int(request.get_json()['amount'])
    cur_player = game.players_profiles[request.get_json()['id']]
    if cur_player.plant_num >= data and cur_player.material_num >= data and cur_player.cash >= (data * 2000):
        cur_player.material_num -= data
        cur_player.cash -= (data * 2000)
        cur_player.fighter_ordered = data
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/build')
def build_order():
    data = request.get_json()['amount']
    cur_player = game.players_profiles[request.get_json()['id']]
    if cur_player.plant_num + len(cur_player.plants_building) + data <= 6 and cur_player.cash >= data * 2500:
        cur_player.plants_building += [0] * data
        cur_player.cash -= (data * 2500)
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/finish')
def finish_turn():
    data = request.get_json()
    cur_player = game.players_profiles[data['id']]
    cur_player.is_finished = True
    game.players_finished += 1
    return jsonify(data=f'Finished')


def game_loop():

    while True:
        if len(game.players_profiles) == game.players_num:
            game.is_started = True
            break

    while game.month_num:
        while True:
            if game.players_finished == game.players_num:
                break

        game.raw_handling()
        game.plane_handling()
        game.fighter_produce()
        game.plant_checker()

        game.month_num -= 1 #new_month
        game.calculate_taxes()
        game.market_level_choice()
        game.calculate_values()
        for player in game.players_profiles.values():
            player.is_finished = False
        game.players_finished = 0
        if game.players_num == 1:
            game.is_ended = True
            break

    if game.players_num > 1:
        capitalizations = dict()
        for id, player in game.players_profiles.items():
            capitalizations[id] = player.calculate_capitalization(game.min_material_price, game.max_fighter_price)

        sorted_caps = sorted(capitalizations.items(), key=lambda item: item[1], reverse=True)
        winner = next(iter(sorted_caps))
        game.players_profiles.clear()
        game.players_profiles[winner[0]] = winner[1]
        game.is_ended = True


if __name__ == "__main__":
    thread = threading.Thread(target=game_loop)
    thread.start()
    server.run(ip, port=port)

