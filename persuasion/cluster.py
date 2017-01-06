import json

from simple_model import Model, Attribute, list_type
import movements

import utils
import agents


def serialize(model):
    attributes = dir(model)
    att_dict = {}
    for attribute in attributes:
        if "__" not in attribute:
            field = (getattr(model, attribute))
            if type(field) == unicode:
                field = field.encode("ascii", "ignore")
            if attribute not in ["members", "add_cluster", "update_happiness"]:
                print attribute, type(attribute)
                att_dict[attribute] = field

    return json.dumps(att_dict)


def deserialize(string):
    return Cluster(**json.loads(string.strip("\n")))


def save_all(clusters, file_path = 'clusters/json/all clusters.txt'):
    with open(file_path, 'w') as f:
        for cluster in clusters:
            print serialize(cluster)
            f.write(serialize(cluster)+"\n")

def append_to_end(Cluster,file_path = 'clusters/json/all clusters.txt'):
    string = serialize(Cluster)
    with open(file_path, 'a') as f:
        f.write(string + "\n")


def load_all(path = 'clusters/json/all clusters.txt'):
    clusters = []
    with open(path, 'r') as f:
        for line in f:
            clusters.append(deserialize(line))
    return clusters

def load_cluster(file_path = 'clusters/json/cluster 0.txt'):
    f = open(file_path)

    string = f.read()
    cluster = deserialize(string)

    f.close()
    return cluster


def parse_rect(string):
    data = string.split(",")
    return utils.get_rect(*data)


def move_cluster(cluster, x, y):
    for position in cluster.positions:
        position[0] += x
        position[1] += y


def change_attitude(cluster, attitude):
    cluster.attitude = attitude


class Cluster:

    def __init__(self, name="", start_positions=[], attitude=0, start_position=-999):
        self.start_positions = start_positions
        self.name = name
        self.attitude = attitude

        self.members = []
        self.add_cluster()
        start = start_position
        for pos in self.start_positions:
            y = pos[1]
            if y > start:
                start = y
            self.start_position = start

    def add_cluster(self, happiness=50, movement=movements.idle, game=None):
        for i in range(len(self.start_positions)):
            self.members.append(
                agents.Agent(self.start_positions[i][0], self.start_positions[i][1], happiness,
                             movement=movement,
                             attitude=self.attitude))
            #game.add_agent(self.members[i])

    def update(self, player):
        for agent in self.members:
            agent.distance_to_player = utils.distance(player.rect, agent.rect)
            if not isinstance(agent, agents.Player):
                if agent.distance_to_player <= agent.width:
                    player.on_collision(agent)
                    agent.on_collision(player)
                if agent.distance_to_player <= agent.personalspace:

                    if (player.happiness > 0) and agent.attitude == agents.Attitude["avoiding"]:
                        player.change_happiness(-0.5)
                    agent.on_enter_personal_space(player)

            agent.update()

    def update_happiness(self):
        for i in range(len(self.members)):
            for j in range(len(self.members)):
                self.members[i].happiness += (self.members[j].happiness - self.members[i].happiness)/100


    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def regroup_wait(self,dx = 0, dy = 0):
        paths = []
        longest_path = 0
        for i in range(len(self.members)):
            target_x = self.starting_positions[i][0] + dx
            target_y = self.starting_positions[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            paths.append(movements.path_direct((target_x - current_x, target_y - current_y)))
            if len(paths[i]) > longest_path:
                longest_path = len(paths[i])

        for i in range(len(self.members)):
            paths[i].extend([[0,0]] * (longest_path - len(paths[i])))
            self.members[i].set_path(paths[i])



    def regroup(self, dx = 0, dy = 0):
        for i in range(len(self.members)):
            target_x = self.starting_positions[i][0] + dx
            target_y = self.starting_positions[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            self.members[i].goal = (target_x - current_x, target_y - current_y)
            self.members[i].set_path(movements.path_direct)

    def save_cluster(self, file_path=''):
        if file_path == '':
            file_path = 'clusters/json/cluster ' + int(self.number) + '.txt'
        string = serialize(self)
        f = open(file_path, 'w')
        f.write(string)
        f.close()
