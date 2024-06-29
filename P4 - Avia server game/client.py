import sys

import requests

import time
import copy
import os


def is_valid_addr(ip):
    if ip.count('.') == 3:
        for i in ip.split('.'):
            if 0 <= int(i) <= 255:
                pass
            else:
                return False
        return True


def set_params():
    if is_valid_addr(sys.argv[1]):
        return [sys.argv[1], sys.argv[2], sys.argv[3]]
    else:
        print('wrong ip')
    return [False]


def order(op_type, info):
    inp = ['raw', 'buy'] if op_type == 'raw' else ['plane', 'sell']
    req = 'buy_raw' if op_type == 'raw' else 'sell_planes'
    while True:
        print(info)
        raw = input(f"How much {inp[0]} you want to {inp[1]}? Input number and price separated by a space If you don't want to buy just press Enter\n")
        if raw == '':
            break
        raw = raw.split()
        if len(raw) == 2:
            response = requests.post(f'{url}{req}', json={'number': raw[0], 'price': raw[1], 'id': pl_id})
            print(response.json()['data'])
            time.sleep(1.5)
            os.system('CLS')
            if response.json()['status'] == 'ok':
                break
        else:
            print('Incorrect input')
            time.sleep(1)
            os.system('CLS')
    return None


def get_info():
    time.sleep(1)
    resp = requests.post(f'{url}info', json={'id': pl_id}).json()
    if resp['status'] == '0':
        return resp['data'], 0
    elif resp['status'] == '10':
        return resp['data'], 10
    elif resp['status'] == '-1':
        return resp['data'], -1
    elif resp['status'] == '1':
        market_lvl, raw_price, plane_price, plants, cash, fighters, raw = resp['market_lvl'], resp['raw_price'], resp['plane_price'], resp['plants'], resp['cash'], resp['fighters'], resp['raw']
        return f"Market level: {market_lvl}\nRaw price: {raw_price}\nPlane price: {plane_price}\n\nPlants: {plants}\nCash: {cash}\nFighters: {fighters}\nRaw: {raw}\n", 1
    elif resp['status'] == '2':
        return resp['data'], 2


def produce_order(op_type, info):
    inp = ['planes', 'produce'] if op_type == 'plane' else ['plants', 'build']
    req = 'produce' if op_type == 'plane' else 'build'
    while True:
        print(info)
        ordr = int(input(f"How many {inp[0]} do you want to {inp[1]}? Enter number or press Enter if you don't want to buy\n"))
        if ordr == '':
            break
        response = requests.post(f'{url}{req}', json={'amount': ordr, 'id': pl_id}).json()
        print(response['data'])
        time.sleep(1.5)
        os.system('CLS')
        if response['status'] == 'ok':
            break
    return None


def finish_turn():
    print(requests.post(f'{url}finish', json={'id':pl_id}).json()['data'])
    return None

params = set_params()
if not params[0]:
    sys.exit()
ip = f'{params[0]}:{params[1]}'

#ip = '127.0.0.1:5000'
url = f"http://{ip}/"
name = params[2]
pl_id = 0
claimed = {'raw': False, 'sell': False, 'produce': False, 'build': False}

while True:
    response = requests.post(f'{url}connect', json={'name': name})
    print(response.json()['data'])
    if response.json()['status'] == 'ok':
        pl_id = response.json()['id']
        break
    time.sleep(1)

os.system('CLS')
while True:
    claimed_copy = copy.deepcopy(claimed)
    while True:
        info, phase = get_info()
        if phase in [0, -1, 2, 10]:
            print(info)
            time.sleep(1)
        elif phase == 1:
            os.system('CLS')
            print(info)
            message = f"1 - buy raw. Done: {claimed_copy['raw']}\n" \
                      f"2 - sell planes. Done: {claimed_copy['sell']}\n" \
                      f"3 - produce planes. Done: {claimed_copy['produce']}\n" \
                      f"4 - build plants. Done: {claimed_copy['build']}\n" \
                      f"5 - Finish turn\n"
            inp = input(message)
            if inp == '1':
                order('raw', info)
                claimed_copy['raw'] = True
            elif inp == '2':
                order('plane', info)
                claimed_copy['sell'] = True
            elif inp == '3':
                produce_order('plane', info)
                claimed_copy['produce'] = True
            elif inp == '4':
                produce_order('plant', info)
                claimed_copy['build'] = True
            if inp == '5':
                finish_turn()
                break
            elif inp == '6':
                sys.exit()
            os.system('CLS')

