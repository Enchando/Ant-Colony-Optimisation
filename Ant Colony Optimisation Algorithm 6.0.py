import random as rn
import numpy as np

def ACOA(bins, items, paths, evap_rate, fitness_evals):
    '''
    Finds the best fitness for the bin packing algorithm, where fitness is the difference between largest and smallest bin.

    Args:
    bins (int) : Number of bins to be used
    items (list(int)) : List of items to be sorted into the bins
    paths (int): Number of ant paths to be taken each fitness evaluation
    evap_rate (float) : Rate at which all nodes evaporate
    fitness_evals (int) : Number of fitness evaluations

    Returns:
    The best path's fitness found on the final evaluation. 

    '''

    # Create the random pheromones on each of the nodes that the ant can take.
    pheromone_paths = [[rn.uniform(0,1) for i in range(len(items))] for x in range(bins)]

    # Used for printing out the current best when running.
    global_best = sum(items)

    # Determining the amount of times to do the evaluations based on the number of paths.
    runs = int(fitness_evals / paths)
    
    for each_run in range(runs):
        
        fitness_list = []
        path_list = []

        for path in range(paths):
            
            path = navigate_path(items, pheromone_paths, bins)

            # Append the path to the path list for this iteration.
            path_list.append(path)
            
            # Get the weights of the bins. 
            bin_list = [0 for y in range(bins)]

            for i in range(len(path)):
                bin_list[path[i]] += items[i]

            #Find the fitness of the individual path.

            fitness_list.append(max(bin_list) - min(bin_list))

        # Update the pheromones for the paths calculated.
        current_path = 0
        for path in path_list:

            current_path_node = 0

            # Calculate the overall fitness of the path.
            pheromone_update = (100 / fitness_list[current_path])

            # Go through each node in the path and update the pheromone in pheromone_paths with the pheromone update. 
            for each_choice in path:

                pheromone_paths[each_choice][current_path_node] += pheromone_update
                current_path_node += 1

            current_path += 1

            each_run += 1
        
        # Final step is to evaporate all nodes in pheromone_paths by the evaporation rate.
        pheromone_paths = evaporate(pheromone_paths, evap_rate)

        # Checking if the fitness for this iteration is better than the global best (not used for actual result)
        if min(fitness_list) < global_best:
            print("New global best found:", min(fitness_list))
            global_best = min(fitness_list)

    print(bin_list)
    return min(fitness_list)
    
    
def navigate_path(items, pheromones, bins): 
    '''
    Method for ant choosing a path based on pheromones.
    
    Args:
    items (list(int)): The items to be placed into the bins
    pheromones (list(list(int))) : The current pheromones for the path nodes. 
    bins (int) : The number of bins

    Returns:
    The path taken by the ant as it navigates its way through the bins

    '''

    path = []

    # Iterate through the items, choosing which bin to put the item in.
    for each_item in range(len(items)):

        # Retrieving the probabilities for the bins next in the ant's path.
        bin_probabilites = [bin_probability[each_item] for bin_probability in pheromones]

        sum_items = sum(bin_probabilites)
        choice = rn.uniform(0, sum_items)
        counter = 0
    
        # Choose a bin based on its probability
        for bin_prob_index in range(len(bin_probabilites)):
            
            counter += bin_probabilites[bin_prob_index]

            if choice <= counter:
                path.append(bin_prob_index)
                break

    return path



def evaporate(pheromones, evap_rate):
    '''
    Evaporates all of the nodes in the pheromone lists.

    Args:
    pheromones (list(list(int))) : The current pheromone list to be updated
    evap_rate (float) : The value which each pheromone needs to be multiplied by.

    Returns:
    The pheromones updated by the evaporation rate.
    '''

    for each_row in pheromones:
        each_row[:] = [(x * evap_rate) for x in each_row]
    
    return pheromones



if __name__ == "__main__":
    print("Example Trial - BPP1 Experiment 1")
    print(ACOA(10, [i + 1 for i in range(500)], 100, 0.90,10000)) # All items added = 124750
    print("Example Trial - BPP2 Experiment 1")
    print(ACOA(50, [(i ** 2 / 2) for i in range(500)], 100, 0.90, 10000)) #All items added = 20770875
    
