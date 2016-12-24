import agents
import movements
from enum import Enum
from agents import Attitude

class Shape(Enum):
    circle = 0
    polygon = 1
    elipse = 2
    rect = 3

class Cluster:


    def __init__(self,members,clustno):
        self.members = members
        self.clustno = clustno

    def create_cluster(self, position, shape, amount, exampleAgent):
        if shape == Shape.circle :
            #dosomething
            print "something"

        for i in range(0,amount):
            self.members[i] = agents.Agent(exampleAgent.x , exampleAgent.y, exampleAgent.color, exampleAgent.screen, exampleAgent.movement, exampleAgent.attitude, exampleAgent.player)


    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def cluster_move(self, agent, speed):
        for idx in range(0,self.members):
            self.members[idx].move(speed)