import numpy as np

class Factors:
    k1 = 0.01 # crosstalk regulation factor for angle cells
    k2 = 0.01 # crosstalk regulation factor for border cells
    k3 = 0.01 # crosstalk regulation factor for center cells
    decay_rate = 0.95 # decay factor for exponential crosstalk reduction

def remove_crosstalk_iterative(data_matrix, max_iterations, tolerance):
    # Assuming data_matrix is a 2D array (i rows,j columns) representing pressure values from the sensor matrix

    corrected_matrix = np.zeros((len(data_matrix),len(data_matrix[0])))
    #corrected matrix initially is all 0 matrix

    for i in range(len(data_matrix)):

        for j in range(len(data_matrix[0])):

            result = data_matrix[i][j]

            for iteration in range(max_iterations+2):

                # Estimate crosstalk using the current result
                crosstalk_estimation = estimate_crosstalk(data_matrix, i, j, iteration)
                #print(f'crosstalk ({i},{j}) estimated= {crosstalk_estimation}')

                # Update result using a fixed-point formulation
                result = np.abs(data_matrix[i][j] - crosstalk_estimation)
                
                # Check for convergence
                if (np.abs(result - data_matrix[i][j])) < tolerance :
                    #print(f'Cell {i},{j} converging')
                    break
                if iteration > max_iterations :
                    #print(f'Cell {i},{j} reached max iteration, NOT converging')
                    break

                data_matrix[i][j] = result
            
            corrected_matrix[i][j] = round(result)
    
    return corrected_matrix

def estimate_crosstalk(data_matrix, i, j, iteration):
# Estimate crosstalk based on nearby cells values

    rows = len(data_matrix)-1
    col = len(data_matrix[0])-1

    k1 = decay_function(Factors.k1, iteration, Factors.decay_rate)
    k2 = decay_function(Factors.k2, iteration, Factors.decay_rate)
    k3 = decay_function(Factors.k3, iteration, Factors.decay_rate)

    # ANGLES
    if (i==0 and j==0): crosstalk_estimation = k1 * (data_matrix[1][0]+data_matrix[0][1]+data_matrix[1][1])/3
    elif (i==rows and j==col): crosstalk_estimation = k1 * (data_matrix[rows-1][col]+data_matrix[rows][col-1]+data_matrix[rows-1][col-1])/3
    elif (i==rows and j==0): crosstalk_estimation = k1 * (data_matrix[rows-1][0]+data_matrix[rows][1]+data_matrix[rows-1][1])/3
    elif (i==0 and j==col): crosstalk_estimation = k1 * (data_matrix[0][col-1]+data_matrix[1][col-1]+data_matrix[1][col])/3
    #BORDERS
    elif (i==0 and j!=0 and j!=col): crosstalk_estimation = k2 * (data_matrix[i][j+1]+data_matrix[i][j-1]+data_matrix[i+1][j])/3
    elif (i==rows and j!=col and j!=0): crosstalk_estimation = k2 * (data_matrix[i][j+1]+data_matrix[i][j-1]+data_matrix[i-1][j])/3
    elif (j==0 and i!=rows and i!= 0): crosstalk_estimation = k2 * (data_matrix[i-1][j]+data_matrix[i+1][j]+data_matrix[i][j+1])/3
    elif (j==col and i!=rows and i!=0): crosstalk_estimation = k2 * (data_matrix[i-1][j]+data_matrix[i+1][j]+data_matrix[i][j-1])/3
    #CENTER
    else: crosstalk_estimation = k3 * (data_matrix[i+1][j]+data_matrix[i][j+1]+data_matrix[i-1][j]+data_matrix[i][j-1])/4

    return crosstalk_estimation
            
def decay_function(initial_value, iteration, decay_rate):
# Exponential reduction for regulation factors

    return initial_value * decay_rate**iteration


# CASUAL MATRIX TEST

original_data = np.random.randint(0, 70, size=(8, 16))

print(f'matrice originale:\n {original_data}')

noise_data = (10) * np.random.rand(8, 16)

noisy_data = original_data + noise_data

print(f'\nmatrice modificata:\n {noisy_data}')

removed_crosstalk_data = remove_crosstalk_iterative(noisy_data,100,0.2)

print(f'\nmatrice dopo rimozione crosstalk:\n {removed_crosstalk_data}')





