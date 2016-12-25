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

class Cluster:


    def __init__(self,clustno,members = [],):
        self.members = members
        self.clustno = clustno

    def distance(self, (x,y), (x2,y2)):
        return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)

    def create_cluster(self, position, shape, amount, exampleAgent, game):
        amountleft = amount
        agent_locations = []
        if shape == Shape.circle:
        try:
                for x in range(position[0] - position[2],position[0] + position[2]):
                    for y in range(position[1] - position[2], position[1] + position[2]):
                        if amountleft > 0:
                            if random.randint(0, amountleft) > 0:
                                if distance((x,y),(position[0],position[1])) <= position[2]:
                                    agent_locations.append([(x,y)])
                                    amountleft = amountleft - 1
                                    raise NoMoreAgents

        except NoMoreAgents:
            for i in range(0,len(locations)):
                self.members[i] = agents.Agent(agent_locations[i][0] , agent_locations[i][1], exampleAgent.color, exampleAgent.screen, exampleAgent.movement, exampleAgent.attitude, exampleAgent.player)
                game.add_agent(self.members[i])

    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def cluster_move(self, agent, speed):
        for idx in range(0,self.members):
            self.members[idx].move(speed)