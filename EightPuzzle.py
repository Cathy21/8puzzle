import random 
import copy

class EightPuzzle():
    def __init__(self):
        """Initializes class"""
        random.seed(50)
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.state = self.goal_state
        self.max_nodes = 10000
    
    def set_state(self, state_input):
        """Set the puzzle state
        
        Args:
            state_input: string in format 'b12 345 678'
        """
        #iterates through the string and sets the state
        for i, row in enumerate(state_input.split(" ")): 
            for j, num in enumerate(row):
                if num == "b":
                    self.state[i][j] = 0
                else:
                    self.state[i][j] = int(num)
      
    def randomize_state(self, n):
        """make n moves from the goal state
        
        Args:
            n: number of moves from the goal state
        """
        state = self.goal_state    
        #Used for loop to iterate and make n random moves  
        for i in range(n):
            directions_allowed, _, _ = self.directions_allowed(state)
            move = random.choice(directions_allowed)
            state = self.move(move, state) 
        #set the state to randomized state
        self.state = state
        print("Randomized State:")
        self.print_state()

    def directions_allowed(self, state):
        """returns the allowed directions of the blank tile and the index of the space

        Args:
            state: state to find the possible moves for
        Returns:
            directions_allowed: a list of directions that the blank tile can perform
            r: row of blank tile
            c: column of blank tile
        """
        #Search for index of blank tile
        for i, row in enumerate(state):
            for j, num in enumerate(row):
                if num == 0:
                    r = i
                    c = j
        directions_allowed = []

        #Apppend available directions to list of directions allowed
        if r == 0:
            directions_allowed.append("down")
        elif r == 1:
            directions_allowed.extend(("up", "down"))
        elif r == 2:
            directions_allowed.append("up")
        if c == 0:
            directions_allowed.append("right")
        elif c == 1:
            directions_allowed.extend(("left", "right"))
        elif c == 2:
            directions_allowed.append("left")
        return directions_allowed, r, c

    def print_state(self):
        """Print the current puzzle state"""
        for row in self.state:
            print(str(row[0]), str(row[1]), str(row[2])) 
            
    def move(self, direction, state):
        """Move the blank tile 'up', 'down', 'left', or 'right'
        
        Args:
            direction: string that describes direction to move blank tile
            state: state to move blank tile
        Returns:
            state: state with moved tile
        """
        directions_allowed, r, c = self.directions_allowed(state)
        new_state = copy.deepcopy(state)
        if direction == "down":
            index = state[r + 1][c]
            new_state[r][c] = index
            new_state[r + 1][c] = 0
        elif direction == "up":
            index = state[r - 1][c]
            new_state[r][c] = index
            new_state[r - 1][c] = 0
        elif direction == "left":
            index = state[r][c - 1]
            new_state[r][c] = index
            new_state[r][c -1] = 0
        elif direction == "right":
            index = state[r][c + 1]
            new_state[r][c] = index
            new_state[r][c + 1] = 0
        return new_state
    
    def h1(self, state):
        """The h1 heuristic which returns the number of misplaced tiles in a given state

        Args:
            state: state to find h1
        Returns:
            misplaced_tiles: returns the number of misplaced tiles in the state
        """
        #create a flat list of the state given and the goal state
        state_2D = sum(state, [])
        goal_2D = sum(self.goal_state, [])
        misplaced_tiles = 0
        #traverse through both states and compare
        for i, j in zip(state_2D, goal_2D):
            if i != j:
                misplaced_tiles += 1
        return misplaced_tiles

    def h2(self, state):
        """The h2 heuristic which returns the sum of the distances of tiles from its goal state

        Args:
            state: state to find h2
        Returns:
            manhattan: sum of the distances of tiles from its goal state
        """
        #Create a flat listof the state given and the goal state
        state_list = {}
        goal_list = {}
        manhattan = 0
        #traverse through both lists to obtain index of each value
        for i, row in enumerate(state):
            for j, num in enumerate(row):
                state_list[num] = (i, j)        
        for i, row in enumerate(self.goal_state):
            for j, num in enumerate(row):
                goal_list[num] = (i, j)
        #Check if tile is in the correct index                
        for tile, index in state_list.items():
            if tile == 0:
                pass
            #Add to manhattan the difference in row index and difference in column index
            else:
                goal_index = goal_list[tile]
                manhattan += (abs(index[0] - goal_index[0]) + abs(index[1] - goal_index[1]))
        return manhattan

    def f(self, cost, state, heuristic):
        """Returns the total cost of the state

        Args:
            cost: cost of moves leading up to state
            state: current state
            heuristic: string describing which heuristic to use to calculate total cost
        Returns:
            total cost of state
        """
        if heuristic == "h2":
            return cost + self.h2(state)
        elif heuristic == "h1":
            return cost + self.h1(state)
        else:
            "ERROR: Not a valid heuristic"
    
    def solve_A_star(self, heuristic):
        """Solves the puzzle from the current state using a A-star search

        Args:
            heuristic: string describing heuristic to use for search
        """
        #Create list of child nodes and already expanded nodes
        child_nodes = {}
        expanded = {}        
        state = copy.deepcopy(self.state)
        node_num = 0
        expanded[node_num] = {"state": state, "parent": "root", "direction": "start", "cost": self.f(0, state, heuristic), "depth": 0}
        child_nodes[node_num] = {"state": state, "parent": "root", "direction": "start", "cost": self.f(0, state, heuristic), "depth": 0}
        fail = False
        #Priority queue
        all_child_nodes = [(0, child_nodes[0]["cost"])]
        #Iterate through nodes
        while not fail:
            current_depth = 0
            #Find depth of node - this is the cost
            for node_num, node in expanded.items():
                if node["state"] == state:
                    current_depth = node["depth"]
            directions_allowed, _, _ = self.directions_allowed(state)
            #Find the directions the blank tile is allowed to move
            for direction in directions_allowed:
                repeat = False
                #Break if number of nodes has exceeded the max to be considered
                if node_num >= self.max_nodes:
                    fail = True
                    print("ERROR: No Solution Found")
                    self.num_nodes = max_nodes
                    break
                #state and parent of next state
                new_state = self.move(direction, state)
                new_parent = copy.deepcopy(state)
                #Check if node has already been expanded
                for node in expanded.values():
                    if node["state"] == new_state:
                        if node["parent"] == new_parent:
                            repeat = True
                #check to see if repeated
                for node in child_nodes.values():
                    if node["state"] == new_state:
                        if node["parent"] == new_parent:
                            repeat = True    
                if repeat:
                    continue
                else:
                    #Add node to lists
                    node_num += 1
                    depth = current_depth + 1
                    new_cost = self.f(depth, new_state, heuristic)
                    all_child_nodes.append((node_num, new_cost))
                    child_nodes[node_num] = {"state": new_state, "parent": new_parent, "direction": direction, "cost": new_cost, "depth": current_depth + 1}
            #sort nodes
            all_child_nodes = sorted(all_child_nodes, key=lambda x: x[1])
            if not fail:
                #select best node and remove
                next_node = all_child_nodes.pop(0)
                next_num = next_node[0]
                next_state = child_nodes[next_num]["state"]
                state = next_state
                #move node from list of child nodes to list of expanded nodes
                expanded[next_num] = (child_nodes.pop(next_num))
                #Check if state is the goal state 
                if self.check(next_state):
                    print("A star search with heuristic ", heuristic)
                    self.solution(expanded, node_num)
                    break 
    
    def check(self, state):
        """Checks if the state given is the goal state

        Args:
            state: state to check 
        Returns:
            boolean indicating if state is the  goal state
        """
        return state == self.goal_state
                    
    def solve_beam(self, k):
        """Solves the puzzle  from its current state using a local beam search with k states

        Args:
            k: number of states considered per iteration
        """
        state = copy.deepcopy(self.state)
        #Check if the current state is already the goal state
        if state == self.goal_state:
            self.solution(node_list={}, num_nodes=0)
        #Create a reference list of the states already created and the index for the list
        all= {}
        node_num = 0
        all[node_num] = {"state": state, "parent": "root", "direction": "start"}
        #Used evaluation function h1+h2 which was used to determine the best state
        score = self.h1(state) + self.h2(state)
        nodes = [(node_num, score)]       
        fail = False
        solved = False
        while not fail:
            #Check if the number of nodes is greater than the max amount of nodes to be considered
            #If number of nodes exceeds max amount, break from the loop
            if node_num >= self.max_nodes:
                fail = True
                print("No Solution Found in first {} generated nodes".format(max_nodes))
                break
            child_nodes = []
            #Iterate through nodes
            for node in nodes:
                repeat = False
                current_state = all[node[0]]["state"]
                directions_allowed, _, _ = self.directions_allowed(current_state)
                #Iterate through possible directions for move
                for direction in directions_allowed:
                    child = self.move(direction, current_state)
                    #Check if node has already been condsidered
                    for node_num, node in all.items():
                        if node["state"] == child:
                            if node["parent"] == current_state:
                                repeat = True
                    #Check if node is the gaol
                    if child == self.goal_state:	
                        all[node_num] = {"state": child, 
                                "parent": current_state, "direction": direction}
                        print("Local Beam Search: ")
                        self.solution(all, node_num)
                        solved = True
                        break
                    #calculate the score of state and add to list of nodes
                    if not repeat:
                        node_num += 1
                        score = (self.h1(child) + self.h2(child))
                        all[node_num] = {"state": child, "parent": current_state, "direction": direction}
                        child_nodes.append((node_num, score))
                    else:
                        continue
            #Sort and choose best child states
            nodes = sorted(child_nodes, key=lambda x: x[1])
            if k < len(nodes):
                nodes = nodes[:k]
            #If solution has been found then break
            if solved == True:
            	break  

    def steps(self, node, node_list, path):
        """Gives a list of the steps to take to get to goal state

        Args:
            node: node to trace
            node_list: list of potential nodes to trace to
            path: current path
        Returns:
            list of directions to get to goal state from state
        """
        #returns the path when it gets at the root node
        if node["parent"] == "root":
            path.append((node["state"], node["direction"]))
            return path
        #If not the root, then add the state and the move direction to the path
        else:
            state = node["state"]
            parent = node["parent"]
            direction = node["direction"]
            path.append((state, direction))
            for node_num, node in node_list.items():
                #recurse using parent of current node
                if node["state"] == parent:
                    return self.steps(node, node_list, path)
                
    def solution(self, node_list, num_nodes):
        """Prints the solution of the puzzle

        Args:
            node_list: list of nodes used in solving the puzzle
            num_nodes: number of node used
        """
        if len(node_list) >= 1:
            #finds the goal node
            for node_num, node in node_list.items():
                if node["state"] == self.goal_state:
                    goal_node = node_list[node_num]
                    break
            #Creates the solution path from the goal to start node
            solution_path = self.steps(goal_node, node_list, path=[(self.goal_state, "goal")])
            num_moves = len(solution_path) - 2
        else:
            solution_path = []
            num_moves = 0        
        #Prints solution
        print("Number of Moves: ", num_moves)
        path = list(map(lambda x: x[1], solution_path[::-1]))
        for move in path:
            self.state = self.move(move, self.state)
            print(move)
            self.print_state()
        print("\n")
        

    def max_nodes(self, n):
        """Sets the maximum number of nodes to be considered
        
        Args:
            n: max number of nodes to be considered
        """
        self.max_nodes = n

def main():
    # game_h1 = EightPuzzle()
    # game_h1.print_state()
    # game_h1.randomize_state(6)
    # game_h1.solve_A_star("h1")

    # game_h2 = EightPuzzle()
    # game_h2.randomize_state(8)
    # game_h2.solve_A_star("h2")

    # game_local = EightPuzzle()
    # game_local.randomize_state(10)
    # game_local.solve_beam(4)
if __name__ == "__main__":
    main()