import agents
import movements
from agents import Attitude

class Cluster:


    def __init__(self,members,clustno):
        self.members = members
        self.clustno = clustno

    def create_cluster(self, amount, x, y, color, screen, movement=movements.idle, attitude=Attitude.neutral, player=None):
        for i in range(0,amount):
            self.members[i] = agents.Agent(x , y, color, screen, movement, attitude, player)


    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def cluster_move(self, agent, speed):
        for idx in range(0,self.members):
            self.members[idx].move(speed)