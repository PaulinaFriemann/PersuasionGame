import agents
import movements
import math
import random
import pickle
from enum import Enum
import settings

class Shape(Enum):
    circle = 0
    polygon = 1
    elipse = 2
    rect = 3
    file = 4


# density will be multiplicated by the space this amount of agents needs. (density * ceil(sqrt(personal_space)))
def initialize_clusters(agentlist, game, n_minagents = 5, n_maxagents = 15,
                        min_personal_space = 9, max_personal_space = 20,
                        min_density = 1, max_density = 1.5,
                        min_space_between_clusters = 3, max_space_between_clusters = 8):

    n_clusters = len(agentlist)
    clusters = []
    clusters_starting_locations = []
    clusters_n_agents = []
    clusters_personal_space = []
    clusters_density = []
    clusters_space_between_clusters = []

    for i in range(n_clusters):
        clusters.append(Cluster(i))
        clusters_n_agents.append(random.randint(n_minagents, n_maxagents))
        clusters_personal_space.append(random.randint(min_personal_space, max_personal_space))
        clusters_density.append(random.uniform(min_density, max_density))
        clusters_space_between_clusters.append(random.uniform(min_space_between_clusters, max_space_between_clusters))

        radius = int(math.ceil(clusters_density[i] * (math.sqrt(clusters_n_agents[i]))*clusters_personal_space[i]))

        if i > 0:
            y = math.ceil(clusters_starting_locations[i - 1][1] - (
            clusters_starting_locations[i - 1][2] * clusters_space_between_clusters[i]))
        else:
            y = 0

        x = random.randint(radius + 4, game.width - (radius + 4))
        clusters_starting_locations.append((x, y, radius))
        with open("clusters/clusterinfos/clusterinfo " + str(i) + ".txt", 'w') as f:
            f.write(str(clusters_n_agents[i]) +  '\n')
            f.write(str(clusters_personal_space[i]) +  '\n')
            f.write(str(clusters_density[i]) +  '\n')
            f.write(str(clusters_space_between_clusters[i]) +  '\n')
            f.write(str(clusters_starting_locations[i]) +  '\n')

    for i in range(len(clusters)):
        clusters[i].create_cluster(clusters_starting_locations[i], clusters_n_agents[i], agentlist[i], game, Shape.circle)
        clusters[i].to_pickle('clusters/pickles/Cluster ' + str(i) + '.cluster')

def circle_map(radius):
    arr_size = (2 * radius) + 1
    map_circle = [[0] * arr_size for _ in range(arr_size)]

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
                except ValueError:
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

    def __init__(self, clustno, members=None, ):
        if members is None:
            members = []
        self.members = members
        self.starting_locations = []
        self.clustno = clustno
        self.map = []
        self.cluster_starting_position = []
        self.possible_coordinates = []
        self.step = 0

    def create_cluster(self, position, amount, exampleAgent, shape=Shape.circle, agent_personal_space = 12, filename = 'map.txt'):
        self.cluster_starting_position = position


        # self.len_default_path = len(exampleAgent.defaultpath)

        necessary_coordinates = []
        if shape == Shape.circle:
            self.map = circle_map(self.cluster_starting_position[2])
            self.possible_coordinates = to_coordinates(self.map, (self.cluster_starting_position[0], self.cluster_starting_position[1]))
            #export_map(self.map,'map.txt')
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
                self.members.append(agents.Agent(location[0], location[1], exampleAgent.color, exampleAgent.default_movement, exampleAgent.attitude, exampleAgent.cluster_member))
                settings.game.add_agent(self.members[i])
        except ValueError:
            print "I am sorry, there is no space left. I could only make " + str(i) + " agent(s)."

    def add_member(self,member):
        self.members.extend(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    # def cluster_move(self, speed):
    #     for idx in range(0,len(self.members)):
    #         self.members[idx].move(speed)
    #         self.step = (self.step + 1) % self.len_default_path

    def regroup_wait(self,dx = 0, dy = 0):
        paths = []
        longest_path = 0
        for i in range(len(self.members)):
            target_x = self.starting_locations[i][0] + dx
            target_y = self.starting_locations[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            paths.append(movements.path_direct((target_x - current_x, target_y - current_y)))
            if len(paths[i]) > longest_path:
                longest_path = len(paths[i])

        for i in range(len(self.members)):
            paths[i].extend([[0,0]] * (longest_path - len(paths[i])))
            self.members[i].set_path(paths[i])


    def regroup(self, dx = 0, dy = 0):
        for i in range(len(self.members)):
            target_x = self.starting_locations[i][0] + dx
            target_y = self.starting_locations[i][1] + dy
            current_x,current_y = self.members[i].rect.center
            self.members[i].goal = (target_x - current_x, target_y - current_y)
            self.members[i].set_path(movements.path_direct)

    def rewrite_map(self):
        arr_size = len(self.map)
        self.map = [[0] * arr_size for _ in range(arr_size)]
        center_x = self.cluster_starting_position[0]
        center_y = self.cluster_starting_position[1]
        radius   = self.cluster_starting_position[2]

        for (x, y) in self.starting_locations:
            self.map[x - center_x + radius][ y - center_y + radius] = 'X'

        for (x,y) in self.possible_coordinates:
            self.map[x - center_x + radius][ y - center_y + radius] = 1

    def to_pickle(self,filename = ""):
        if filename == "":
            filename = str(self.clustno) + ".cluster"
        with open(filename,"wb") as f:
            #pickle.dump(self.members,f)
            pickle.dump(self.starting_locations,f)
            pickle.dump(self.clustno,f)
            pickle.dump(self.map,f)
            pickle.dump(self.cluster_starting_position,f)
            pickle.dump(self.possible_coordinates,f)
            pickle.dump(self.step,f)


    def from_pickle(self,filename,exampleAgent):
        with open(filename,"rb") as f:
            #self.members = pickle.load(f)
            self.starting_locations = pickle.load(f)
            self.clustno = pickle.load(f)
            self.map = pickle.load(f)
            self.cluster_starting_position = pickle.load(f)
            self.possible_coordinates = pickle.load(f)
            self.step = pickle.load(f)
        self.members = []
        for i in range(len(self.starting_locations)):
            self.members.append(
                agents.Agent(self.starting_locations[i][0], self.starting_locations[i][1], exampleAgent.color, exampleAgent.screen, exampleAgent.movement,
                             exampleAgent.attitude, exampleAgent.cluster_member, exampleAgent.player))
            settings.game.add_agent(self.members[i])

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

