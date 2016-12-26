import agents
import movements
import math
import random
from enum import Enum
from agents import Attitude

class Shape(Enum):
    circle = 0
    polygon = 1
    elipse = 2
    rect = 3

def circle_map(radius):
    arr_size = (2 * radius) + 1
    map_circle = [[0] * (arr_size) for _ in range(arr_size)]

    for x in range(arr_size):
        for y in range(arr_size):
            if distance((x,y),(radius,radius)) <= radius:
                map_circle[x][y] = '1'

    return map_circle

def distance((x,y), (x2,y2)):
    return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)

def to_coordinates(map, (center_x, center_y)):
    coordinates = []
    radius = len(map)/2
    for x in range(len(map)):
        for y in range(len(map)):
            if map[x][y]:
                coordinates.append((center_x - radius + x, center_y - radius + y))

    return coordinates


class Cluster:

    def __init__(self,clustno,members = [],):
        self.members = members
        self.clustno = clustno



    def create_cluster(self, position, amount, exampleAgent, game, shape=Shape.circle, agent_personal_space = 10, map = []):

        if shape == Shape.circle:
            map = circle_map(position[2])

        possible_coordinates = to_coordinates(map,(position[0],position[1]))
        #print possible_coordinates
        for i in range(amount):
            lottery = random.randint(1,len(possible_coordinates)) - 1
            location = possible_coordinates[lottery]

            erradicate_coordinates = to_coordinates(circle_map(agent_personal_space),location)

            for erradicate in erradicate_coordinates:
                if erradicate in possible_coordinates:
                    possible_coordinates.remove(erradicate)

            self.members.append(agents.Agent(location[0], location[1], exampleAgent.color, exampleAgent.screen, exampleAgent.movement, exampleAgent.attitude, exampleAgent.player))
            game.add_agent(self.members[i])

    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def cluster_move(self, agent, speed):
        for idx in range(0,self.members):
            self.members[idx].move(speed)