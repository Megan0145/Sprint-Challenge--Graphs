from room import Room
from player import Player
from world import World
from queue import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

# Step 1: initialise graph 
graph = {}

# Add the first room the player is in to graph with the room id as the key and an empty dictionary to hold key-value pairs for every possible exit. 
graph[player.current_room.id] = {}

# For every possible exit from the starting room, add a key-value pair to the starting room dictionary with the exit as the key and a '?' as the value since we 
# don't know the id of the room through each possible exit just yet. 
# For example: if possible exits for the starting room = ['n', 's', 'e', 'w'], then graph will initally be { 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'} }
for exit in player.current_room.get_exits():
    graph[player.current_room.id][exit] = '?'
   
# Step 2: Add function to get unexplored paths from player's current room
def get_unexplored_paths(room):
    for exit in room:
        if room[exit] == '?':
            return exit
        else:
            return None   

# Step 3: Add helper function that returns whether there are still rooms in the graph that have not been visited.
# This can be found by looping over the graph dictionary. For every room in the graph, if the dictionary holding the exits for that room contains a '?', then there are still 
# paths left unexplored in the graph
def unexplored_paths_exist(graph):
    for room in graph:
        if '?' in graph[room].values():
            return True
        else: False

reverse_directions = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

# Step 4: While the graph is unexplored we want to continue traversing it:
while unexplored_paths_exist(graph):
    # save current room in variable
    current_room = player.current_room
    # if there are unexplored paths in the graph dictionary at the index of the current room..  
    direction = get_unexplored_paths(graph[current_room.id])
    if direction is not None:
        # get the room in that direction by calling the get_room_in_direction() method on room class
        next_room = current_room.get_room_in_direction(direction)
        # add the id of the room in that direction to the graph dictionary at the index of the current room
        graph[current_room.id][direction] = next_room.id
        # check if next room is already in graph and if not add it..
        if not next_room.id in graph:
            graph[next_room.id] = {}
            # get exits for next room, initialise to '?'
            for exit in next_room.get_exits():
                graph[next_room.id][exit] = '?'
            # add current room id in the reverse direction of where you have to go to get to the next room
            graph[next_room.id][reverse_directions[direction]] = current_room.id
        # travel there
        player.travel(direction)        
        # and add the direction to the traversal_path
        traversal_path.append(direction)





# TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for direct in player.current_room:
#     print(player.current_room[direct])

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f'TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited')
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f'{len(room_graph) - len(visited_rooms)} unvisited rooms')



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
