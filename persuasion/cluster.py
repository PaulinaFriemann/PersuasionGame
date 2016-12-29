import agents
import movements
import math
import random
from enum import Enum

class Shape(Enum):
    circle = 0
    polygon = 1
    elipse = 2
    rect = 3
    file = 4

def circle_map(radius):
    arr_size = (2 * radius) + 1
    map_circle = [[0] * (arr_size) for _ in range(arr_size)]

    for x in range(arr_size):
        for y in range(arr_size):
            if distance((x,y),(radius,radius)) <= radius:
                map_circle[x][y] = '1'

    return map_circle

def export_map (map, filename):
    arr_size = len(map)
    with open(filename,'w') as map_file:
        map_file.write('0')
        map_file.write('\n')
        map_file.write(str(arr_size))
        for x in range(arr_size):
            map_file.write('\n')
            for y in range(arr_size):
                map_file.write(str(map[x][y]))

def import_map(filename):
    map = []
    with open(filename,'r') as map_file:
        agents = int(map_file.readline())
        print agents
        arr_size = int(map_file.readline())
        print arr_size

        for x in range(arr_size):
            map.append([])
            for y in map_file.readline().strip():
                try:
                    map[x].append(int(y))
                except (ValueError):
                    map[x].append(y)

    return [map, agents]


def distance((x,y), (x2,y2)):
    return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)


def to_coordinates(map, (center_x, center_y), agents=False):
    coordinates = []
    radius = len(map) / 2
    if agents:
        necessary = []
        for x in range(len(map)):
            for y in range(len(map)):
                if map[x][y] == 'X':
                    necessary.append((center_x - radius + x, center_y - radius + y))
                elif map[x][y]:
                    coordinates.append((center_x - radius + x, center_y - radius + y))
        return [coordinates, necessary]
    else:
        for x in range(len(map)):
            for y in range(len(map)):
                if map[x][y]:
                    coordinates.append((center_x - radius + x, center_y - radius + y))

    return coordinates


class Cluster:

    def __init__(self,clustno,members = [],):
        self.members = members
        self.starting_locations = []
        self.clustno = clustno
        self.map = []
        self.cluster_starting_position = []
        self.possible_coordinates = []
        self.step = 0

    def create_cluster(self, position, amount, exampleAgent, game, shape=Shape.circle, agent_personal_space = 12, filename = 'map.txt'):
        self.cluster_starting_position = position


        self.len_default_path = len(exampleAgent.defaultpath)

        necessary_coordinates = []
        if shape == Shape.circle:
            self.map = circle_map(self.cluster_starting_position[2])
            self.possible_coordinates = to_coordinates(self.map, (self.cluster_starting_position[0], self.cluster_starting_position[1]))
            export_map(self.map,'map.txt')
        if shape == Shape.file:
            self.map, contains_agents = import_map(filename)
            if contains_agents:
                [self.possible_coordinates, necessary_coordinates] = to_coordinates(self.map,(self.cluster_starting_position[0],self.cluster_starting_position[1]),True)
            else:
                self.possible_coordinates = to_coordinates(self.map,(self.cluster_starting_position[0],self.cluster_starting_position[1]))
        try:
            for i in range(amount):
                # can be optimized by creating two seperate for-loops.
                if i < len(necessary_coordinates):
                    location = necessary_coordinates[i]
                else:
                    lottery = random.randint(1,len(self.possible_coordinates)) - 1
                    location = self.possible_coordinates[lottery]

                erradicate_coordinates = to_coordinates(circle_map(agent_personal_space),location)

                for erradicate in erradicate_coordinates:
                    if erradicate in self.possible_coordinates:
                        self.possible_coordinates.remove(erradicate)

                self.starting_locations.append(location)
                self.members.append(agents.Agent(location[0], location[1], exampleAgent.color, exampleAgent.screen, exampleAgent.movement, exampleAgent.attitude, exampleAgent.player))
                game.add_agent(self.members[i])
        except(ValueError):
            print "I am sorry, there is no space left. I could only make " + str(i) + " agent(s)."
    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def cluster_move(self, agent, speed):
        for idx in range(0,len(self.members)):
            self.members[idx].move(speed)
            self.step = (self.step + 1) % self.len_default_path

    def regroup(self, dx = 0, dy = 0):
        for i in range(len(self.members)):
            target_x = self.starting_locations[i][0] + dx
            target_y = self.starting_locations[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            self.members[i].set_path(movements.path_direct((target_x - current_x, target_y - current_y)))

    def rewrite_map(self):
        arr_size = len(self.map)
        self.map = [[0] * (arr_size) for _ in range(arr_size)]
        center_x = self.cluster_starting_position[0]
        center_y = self.cluster_starting_position[1]
        radius   = self.cluster_starting_position[2]

        for (x, y) in self.starting_locations:
            self.map[x - center_x + radius][ y - center_y + radius] = 'X'

        for (x,y) in self.possible_coordinates:
            self.map[x - center_x + radius][ y - center_y + radius] = 1


    def export_cluster(self, filename):
        arr_size = len(self.map)
        self.rewrite_map()

        with open(filename,'w') as map_file:
            map_file.write('1')
            map_file.write('\n')
            map_file.write(str(arr_size))
        
            for x in range(arr_size):
                map_file.write('\n')
                for y in range(arr_size):
                    map_file.write(str(self.map[x][y]))

