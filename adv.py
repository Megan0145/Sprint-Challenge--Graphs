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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
    direction = None
    for exit in room:
        if room[exit] == '?':
           direction = exit
           break
    return direction       

reverse_directions = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

def convert_ids_to_directions(room_id_1, room_id_2):
    if graph[room_id_1].get('s') is not None and graph[room_id_1].get('s') == room_id_2:
        return 's'
    if graph[room_id_1].get('n') is not None and graph[room_id_1].get('n') == room_id_2:  
        return 'n'  
    if graph[room_id_1].get('w') is not None and graph[room_id_1].get('w') == room_id_2: 
        return 'w'  
    if graph[room_id_1].get('e') is not None and graph[room_id_1].get('e') == room_id_2:  
        return 'e'     

# Step 4: While the graph is unexplored we want to continue traversing it:
while len(world.rooms) > len(graph):
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
    # else we have reached a dead end - we're in a room that has no unexplored paths and need to perform a bfs to find the nearest room with unexplored paths
    else:   
        # initialise the queue
        q = Queue()
        # enqueue path initially containing the id of the current room to the queue
        q.enqueue([current_room.id])
        # initalise visited dictionary to store rooms that have already been visited
        visited = set()
        # while queue is not empty
        while q.size() > 0:
            # dequeue first path in queue 
            path = q.dequeue()
            # get the room id from the last element in the path
            room_id = path[-1]       
            # check if there are any unexplored paths to visit in current room
            direction = get_unexplored_paths(graph[room_id])
            # if it returns None then we are in a room with no unexplored paths ...
            if direction is None:
                # if the room hasn't already been visited, add it to the visited set
                if room_id not in visited:
                    # add it to the visited set
                    visited.add(room_id)
                    # for every exit in the current room..
                    for exit in graph[room_id]:
                        # copy over the current contents of the path
                        new_path = list(path)
                        # append the id at that exit to the new path
                        new_path.append(graph[room_id][exit])
                        # add the new path to the queue
                        q.enqueue(new_path)
            
            # else there is an unexplored path at the current room        
            else:
                # we want to break out of bfs but first will need to convert room ids in path to directions:
                # declare empty list to hold directions  
                directions = []       
                # loop in range 0 to the length of the path -1
                for i in range(0, len(path) - 1):
                    # pass the value of the path at index i and the value of the path at index i + 1 into convert_ids_to_directions helper function
                    direction = convert_ids_to_directions(path[i], path[i + 1])
                    # append the result to the directions list
                    directions.append(direction)
                # then for every direction in directions list..
                for d in directions: 
                    # make the player travel in that direction
                    player.travel(d)

                # finally extend the traversal path list with the directions in directions list     
                traversal_path.extend(directions)
                # break out of bfs 
                break                     

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    print(move)
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f'TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited')
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f'{len(room_graph) - len(visited_rooms)} unvisited rooms')



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
