from room import Room
from player import Player
from world import World

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
# traversal_path = ['n', 'n']

# Step 1: initialise graph 
graph = {}

# add the first room the player is in to graph with the id as the key and a dictionary to hold the rooms to the north, south, east and west
# this will initally take the form of: { 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'} }, since we don't know the ids of the rooms to the n, s, e and w yet (if they exist)
graph[player.current_room.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}



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
