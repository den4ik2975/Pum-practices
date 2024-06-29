import signal
import os
import random
import asyncio
import sys
import time

import matplotlib.pyplot as plt
import pygame
from pygame import gfxdraw

station_nums = [0, 1, 2, 3, 4]
ways = {
    0: 'Rikosovskaya',
    7: 'Sobornaya',
    11: 'Crustall',
    14: 'Zarechnaya',
    22: 'Biblioteka '
}
BOOST = 200
passengers_on_station = []
passengers_on_trains = []
timer = [0]
time_passengers = 0
number_of_passengers = 1
pygame.init()
tstart = time.time()
train_icon = pygame.transform.scale(pygame.image.load('./src/train_icon.png'), (64, 64))
troll = pygame.transform.scale(pygame.image.load('./src/aga.png'), (410, 410))
#troll = pygame.transform.scale(pygame.image.load('src/afonin.png'), (410, 410))
train_icon_back = pygame.transform.flip(train_icon, True, False)
log_font = pygame.font.Font('./src/log_font.ttf', 25)
naming_font = pygame.font.Font('./src/naming_font.ttf', 15)
line_color = tuple(int('429bdb'[i:i + 2], 16) for i in (0, 2, 4))
circle_color = tuple(int('2b5378'[i:i + 2], 16) for i in (0, 2, 4))
text_color = tuple(int('e4ecf2'[i:i + 2], 16) for i in (0, 2, 4))
text_color_2 = tuple(int('3b82f6'[i:i + 2], 16) for i in (0, 2, 4))



class Passenger:
    def __init__(self, stations):
        self.dest = random.choice(stations)
        self.time_start = time.time()


class Train:
    def __init__(self, capacity, number):
        self.capacity = capacity
        self.station: Station = None
        self.position = -1
        self.passengers = []
        self.front = True
        self.number = number

    async def passengers_drop(self):
        global time_passengers
        global number_of_passengers
        new_list = self.passengers[:]

        for passenger in self.passengers:
            if passenger.dest == self.station.number:
                time_passengers += (time.time() - passenger.time_start) * BOOST
                number_of_passengers += 1
                del new_list[new_list.index(passenger)]

        self.passengers = new_list[:]

    async def passengers_boarding(self):
        for passenger in self.station.passengers:
            if self.front is True:
                if passenger.dest > self.station.number and self.capacity > len(self.passengers):
                    self.passengers.append(passenger)
                    del self.station.passengers[self.station.passengers.index(passenger)]

            elif self.front is False:
                if passenger.dest < self.station.number and self.capacity > len(self.passengers):
                    self.passengers.append(passenger)
                    del self.station.passengers[self.station.passengers.index(passenger)]

    async def train_on_station(self):
        self.station = ways[self.position]
        if self.position == list(ways.keys())[-1]:
            self.front = False
        if self.position == list(ways.keys())[0]:
            self.front = True
        await self.passengers_drop()
        await self.passengers_boarding()
        await asyncio.sleep(15 / BOOST)
        await asyncio.sleep(60 / BOOST)
        self.position += 1 if self.front is True else -1

    async def move(self):
        print(f'Train {self.number} started')
        while True:
            if self.position not in list(ways.keys()):
                await asyncio.sleep(60 / BOOST)
                self.position += 1 if self.front is True else -1

            elif self.position in list(ways.keys()):
                await self.train_on_station()


class Station:
    def __init__(self, n, name):
        self.name = name
        self.passengers = []
        self.number = n
        self.stations = [i for i in range(len(ways))]
        del self.stations[self.number]

    async def generate_passengers(self):
        while True:
            self.passengers.append(Passenger(self.stations))
            await asyncio.sleep(1 / BOOST)


loop = asyncio.get_event_loop()
t = time.time()
for i in range(len(ways.keys())):
    ways[list(ways.keys())[i]] = Station(i, ways[list(ways.keys())[i]])
train_number = int(input('Количество поездов: '))
interval = ((38 * 60) / train_number) / BOOST
trains = [Train(400, i + 1) for i in range(train_number)]


def term_handler(*args, **kwargs):
    plt.plot(timer[1:], passengers_on_trains, label='On train')
    plt.plot(timer[1:], passengers_on_station, label='On station')
    plt.show()
#    print(f'Average passenger time: {(time_passengers / number_of_passengers).__round__(2)}')
    exit()


async def graphs():
    global passengers_on_station
    global passengers_on_trains
    global timer
    while True:
        passengers_on_station += [sum(len(station.passengers) for station in ways.values()) / 5]
        passengers_on_trains += [sum(len(train.passengers) for train in trains) / train_number]
        timer += [timer[-1] + 1]
        await asyncio.sleep(60 / BOOST)


async def visualize():
    running = True
    screen = pygame.display.set_mode((1220, 640))
    pygame.display.set_caption('Metro vrum vrum')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                term_handler()

        screen.fill('#0e1621')

        pygame.draw.line(screen, line_color, (60, 100), (1200 - 60, 100), 3)
        for pos, station in ways.items():
            gfxdraw.filled_circle(screen, 60 + (pos * 49), 100, 20, circle_color)

            s = naming_font.render(station.name, True, text_color)
            screen.blit(s, (60 + (pos * 49) - s.get_width() // 2, 100 + s.get_height() + 6))

            p = naming_font.render(str(len(station.passengers)), True, text_color)
            screen.blit(p, (60 + (pos * 49) - p.get_width() // 2, 100 + p.get_height() // 2 - 18))

        for train in trains:
            x = (train.position * 49) + train_icon.get_width() / 2

            image = train_icon if train.front is True else train_icon_back
            y = 150 if train.front is True else 10
            offset = (image.get_height() - 6) if train.front is True else -6

            screen.blit(image, (x, y))

            count = str(len(train.passengers))
            t = naming_font.render(count, True, text_color_2)
            screen.blit(t, (x + image.get_width(), y + offset))

        t = log_font.render(f'Time after start: {time.time() - tstart:.2f}s ({(time.time() - tstart) * BOOST:.2f}s on real)', True, text_color)
        screen.blit(t, (10, 300))

        s = f'Trains: {train_number}'
        s += f' -> All started' if trains[-1].position != -1 else ''
        t = log_font.render(s, True, text_color)
        screen.blit(t, (10, 360))

        s = f'Stations: {len(ways)}'
        s += f' -> Started generating' if len(ways[0].passengers) > 0 else ''
        t = log_font.render(s, True, text_color)
        screen.blit(t, (10, 420))
        t = log_font.render(f'Average travelling time(s): {(time_passengers / number_of_passengers).__round__(2)}', True, text_color)
        screen.blit(t, (10, 480))

        screen.blit(troll, (650, 230))

        await asyncio.sleep(1 / 50)
        pygame.display.flip()


async def main():
    global tstart
    loop.create_task(visualize())
    for train in trains:
        loop.create_task(train.move())
        await asyncio.sleep(interval)

    await asyncio.sleep((18 * 60) / BOOST)

    for station in ways.values():
        loop.create_task(station.generate_passengers())
    loop.create_task(graphs())

signal.signal(signal.SIGINT, term_handler)
loop.create_task(main())
loop.run_forever()
