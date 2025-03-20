# mouse_analysis/distance.py

import numpy as np

def euclidean_moving_distance(locations):
    """
    Calculate the total Euclidean moving distance given a 2xn array of mouse positions.
    
    Parameters:
        locations (np.ndarray): A 2xn numpy array where each column is a [x, y] position.
        
    Returns:
        float: Total Euclidean distance traveled.
    """
    if locations.shape[0] != 2:
        raise ValueError("Input array must be of shape 2xn where each column is an [x, y] coordinate.")
    
    # Calculate differences between consecutive points along columns
    differences = np.diff(locations, axis=1)
    
    # Compute Euclidean distances for each step
    step_distances = np.sqrt(np.sum(differences**2, axis=0))
    
    # Sum the step distances to get the total distance traveled
    total_distance = np.sum(step_distances)
    
    return total_distance

# Example usage
if __name__ == "__main__":
    # Create a sample 2xn array: two rows, n columns
    positions = np.array([[0, 3, 6],   # x coordinates
                          [0, 4, 8]])  # y coordinates
    print("Total Euclidean Distance:", euclidean_moving_distance(positions))
